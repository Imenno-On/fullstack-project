-- SQL скрипт для проверки состояния таблицы generated_forms

-- Проверить структуру таблицы
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'generated_forms'
ORDER BY ordinal_position;

-- Проверить все формы и их owner_id
SELECT id, title, owner_id, created_at
FROM generated_forms
ORDER BY created_at DESC;

-- Найти формы без owner_id (если nullable=True)
SELECT id, title, owner_id, created_at
FROM generated_forms
WHERE owner_id IS NULL;

-- Подсчитать формы по owner_id
SELECT owner_id, COUNT(*) as form_count
FROM generated_forms
GROUP BY owner_id;

-- Проверить пользователей
SELECT id, email, full_name
FROM users;

