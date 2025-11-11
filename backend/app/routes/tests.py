from typing import List

from fastapi import APIRouter, HTTPException, status

from app.database import TESTS
from app.models.test_model import Test, TestCreate, TestUpdate

router = APIRouter(prefix="/tests", tags=["Tests"])

# CREATE
@router.post("/", response_model=Test, status_code=status.HTTP_201_CREATED)
def create_test(test_data: TestCreate):
    new_id = max([t.id for t in TESTS], default=0) + 1
    new_test = Test(id=new_id, **test_data.dict())
    TESTS.append(new_test)
    return new_test

# READ ALL
@router.get("/", response_model=List[Test])
def get_all_tests():
    return TESTS

# READ ONE
@router.get("/{test_id}", response_model=Test)
def get_test(test_id: int):
    for test in TESTS:
        if test.id == test_id:
            return test
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")

# UPDATE
@router.put("/{test_id}", response_model=Test)
def update_test(test_id: int, updated_data: TestUpdate):
    for i, test in enumerate(TESTS):
        if test.id == test_id:
            current_data = test.model_dump()
            update_payload = updated_data.model_dump(exclude_unset=True)

            if "completed" in update_payload and "students" not in update_payload:
                # validate completed <= students using existing total
                if update_payload["completed"] > current_data["students"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="completed cannot exceed students",
                    )

            if "students" in update_payload and "completed" not in update_payload:
                if current_data["completed"] > update_payload["students"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="completed cannot exceed students",
                    )

            merged = {**current_data, **update_payload, "id": test_id}
            TESTS[i] = Test(**merged)
            return TESTS[i]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
    )

# DELETE
@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test(test_id: int):
    for test in TESTS:
        if test.id == test_id:
            TESTS.remove(test)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
