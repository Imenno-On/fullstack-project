from typing import List
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.test import Test
from app.schemas.test_schema import TestCreate, TestUpdate, TestResponse
from app.core.dependencies import get_current_user
from app.models.user import User

from app.services.llm_service import generate_questions_from_text
from app.services.google_forms_service import create_google_form
from app.models.generated_form import GeneratedForm
from app.schemas.generated_form_schema import GenerateTestRequest, GeneratedFormResponse

router = APIRouter(prefix="/tests", tags=["Tests"])

# ---------- CREATE ----------
@router.post("/", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_data: TestCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_test = Test(**test_data.dict(), owner_id=current_user.id)
    session.add(new_test)
    await session.commit()
    await session.refresh(new_test)
    return new_test

# ---------- READ (list) ----------
@router.get("/", response_model=List[TestResponse])
async def list_tests(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(select(Test).where(Test.owner_id == current_user.id))
    return res.scalars().all()

# ---------- READ (single) ----------
@router.get("/{test_id}", response_model=TestResponse)
async def get_test(
    test_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == current_user.id)
    )
    test = res.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

# ---------- UPDATE ----------
@router.put("/{test_id}", response_model=TestResponse)
async def update_test(
    test_id: int,
    payload: TestUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == current_user.id)
    )
    test = res.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(test, field, value)
    await session.commit()
    await session.refresh(test)
    return test

# ---------- DELETE ----------
@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(
    test_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await session.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == current_user.id)
    )
    test = res.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    await session.delete(test)
    await session.commit()

# Настройка логирования
logger = logging.getLogger(__name__)


# ---------- GENERATE ----------
@router.post(
    "/generate",
    response_model=GeneratedFormResponse,
    responses={
        400: {"description": "Некорректные данные запроса"},
        429: {"description": "Превышен лимит запросов"},
        500: {"description": "Внутренняя ошибка сервера"},
        503: {"description": "Сервис недоступен"},
    },
    summary="Генерация теста на основе текста",
    description="Создает интерактивный тест на основе предоставленного текста с использованием LLM и Google Forms"
)
async def generate_test(
        payload: GenerateTestRequest,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    start_time = datetime.utcnow()
    logger.info(
        f"Начало генерации теста для пользователя {current_user.id}, длина текста: {len(payload.text)} символов")

    try:
        # Валидация входных данных
        if not payload.text or not payload.text.strip():
            logger.warning(f"Пустой текст от пользователя {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст для генерации теста не может быть пустым"
            )

        # 1. Генерируем вопросы через LLM
        try:
            questions = await generate_questions_from_text(payload.text)
            logger.info(f"Сгенерировано {len(questions)} вопросов для пользователя {current_user.id}")

            if not questions:
                logger.warning(f"LLM вернул пустой список вопросов для пользователя {current_user.id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Не удалось сгенерировать вопросы. Попробуйте другой текст."
                )

            if len(questions) < 3:
                logger.warning(f"Слишком мало вопросов ({len(questions)}) для пользователя {current_user.id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Сгенерировано слишком мало вопросов ({len(questions)}). Нужно минимум 3."
                )

        except Exception as e:
            logger.error(f"Ошибка генерации вопросов: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис генерации вопросов временно недоступен. Попробуйте позже."
            )

        # 2. Создаем информативное название теста
        title_keywords = payload.text.strip().split()[:5]
        form_title = f"Тест: {' '.join(title_keywords)}"
        if len(form_title) > 100:
            form_title = form_title[:97] + "..."

        # 3. Создаем форму в Google Forms
        try:
            form_urls = await create_google_form(
                title=form_title,
                questions=questions
            )

            logger.info(
                f"Создана Google Form: Published URL: {form_urls['published_url']}, Edit URL: {form_urls['edit_url']}")

        except Exception as e:
            logger.error(f"Ошибка создания Google Form: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис Google Forms временно недоступен. Попробуйте позже."
            )

        # 4. Сохраняем в БД
        try:
            db_form = GeneratedForm(
                title=form_title,
                published_url=form_urls["published_url"],
                edit_url=form_urls["edit_url"],
                owner_id=current_user.id,
                question_count=len(questions),
                original_text=payload.text[:500] + "..." if len(payload.text) > 500 else payload.text
            )
            session.add(db_form)
            await session.commit()
            await session.refresh(db_form)

            logger.info(f"Форма сохранена в БД с ID {db_form.id} для пользователя {current_user.id}")

        except Exception as e:
            logger.error(f"Ошибка сохранения в БД: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка сохранения данных. Форма была создана, но не сохранена в базе данных."
            )

        # Логирование времени выполнения
        duration = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"Генерация теста завершена за {duration:.2f} секунд для пользователя {current_user.id}")

        return GeneratedFormResponse(
            published_url=form_urls["published_url"],
            edit_url=form_urls["edit_url"],
            question_count=len(questions),
            title=form_title,
            created_at=datetime.utcnow()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Необработанная ошибка при генерации теста для пользователя {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера. Пожалуйста, попробуйте позже."
        )
