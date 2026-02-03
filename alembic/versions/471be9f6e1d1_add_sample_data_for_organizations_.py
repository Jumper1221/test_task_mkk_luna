"""add_sample_data_for_organizations_buildings_activities

Revision ID: 471be9f6e1d1
Revises: 6ffac3014940
Create Date: 2026-02-03 19:06:01.483986

"""

from typing import Sequence, Union

from sqlalchemy import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "471be9f6e1d1"
down_revision: Union[str, Sequence[str], None] = "6ffac3014940"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert sample activities with hierarchical structure
    op.execute(
        text("""
        INSERT INTO activities (id, name, parent_id, level, created_at, updated_at) VALUES
        (1, 'Еда', NULL, 1, NOW(), NOW()),
        (2, 'Мясная продукция', 1, 2, NOW(), NOW()),
        (3, 'Молочная продукция', 1, 2, NOW(), NOW()),
        (4, 'Автомобили', NULL, 1, NOW(), NOW()),
        (5, 'Грузовые', 4, 2, NOW(), NOW()),
        (6, 'Легковые', 4, 2, NOW(), NOW()),
        (7, 'Запчасти', 6, 3, NOW(), NOW()),
        (8, 'Аксессуары', 6, 3, NOW(), NOW()),
        (9, 'Образование', NULL, 1, NOW(), NOW()),
        (10, 'Школы', 9, 2, NOW(), NOW()),
        (11, 'ВУЗы', 9, 2, NOW(), NOW()),
        (12, 'Курсы', 9, 2, NOW(), NOW()),
        (13, 'Медицина', NULL, 1, NOW(), NOW()),
        (14, 'Стоматология', 13, 2, NOW(), NOW()),
        (15, 'Хирургия', 13, 2, NOW(), NOW()),
        (16, 'Терапия', 13, 2, NOW(), NOW()),
        (17, 'Фармацевтика', 13, 2, NOW(), NOW()),
        (18, 'Технологии', NULL, 1, NOW(), NOW()),
        (19, 'Программирование', 18, 2, NOW(), NOW()),
        (20, 'Консалтинг', 18, 2, NOW(), NOW()),
        (21, 'IT-оборудование', 18, 2, NOW(), NOW()),
        (22, 'Строительство', NULL, 1, NOW(), NOW()),
        (23, 'Жилищное строительство', 22, 2, NOW(), NOW()),
        (24, 'Промышленное строительство', 22, 2, NOW(), NOW()),
        (25, 'Ремонтные работы', 22, 2, NOW(), NOW())
    """)
    )

    # Insert sample buildings with geometry points
    op.execute(
        text("""
        INSERT INTO buildings (id, address, location, created_at, updated_at) VALUES
        (1, 'г. Москва, ул. Тверская, д. 6', ST_SetSRID(ST_MakePoint(37.6173, 55.7558), 4326), NOW(), NOW()),
        (2, 'г. Москва, ул. Арбат, д. 10', ST_SetSRID(ST_MakePoint(37.5961, 55.7521), 4326), NOW(), NOW()),
        (3, 'г. Москва, Новинский бульвар, д. 8', ST_SetSRID(ST_MakePoint(37.5881, 55.7551), 4326), NOW(), NOW()),
        (4, 'г. Москва, ул. Садовническая, д. 82', ST_SetSRID(ST_MakePoint(37.6225, 55.7338), 4326), NOW(), NOW()),
        (5, 'г. Москва, ул. Ленинградский пр-т, д. 39', ST_SetSRID(ST_MakePoint(37.5440, 55.7958), 4326), NOW(), NOW()),
        (6, 'г. Санкт-Петербург, Невский проспект, д. 28', ST_SetSRID(ST_MakePoint(30.3158, 59.9343), 4326), NOW(), NOW()),
        (7, 'г. Санкт-Петербург, ул. Рубинштейна, д. 14', ST_SetSRID(ST_MakePoint(30.3492, 59.9288), 4326), NOW(), NOW()),
        (8, 'г. Санкт-Петербург, ул. Большая Конюшенная, д. 9', ST_SetSRID(ST_MakePoint(30.3208, 59.9308), 4326), NOW(), NOW()),
        (9, 'г. Новосибирск, ул. Красный проспект, д. 35', ST_SetSRID(ST_MakePoint(82.9346, 55.0415), 4326), NOW(), NOW()),
        (10, 'г. Новосибирск, ул. Советская, д. 22', ST_SetSRID(ST_MakePoint(82.8982, 55.0291), 4326), NOW(), NOW()),
        (11, 'г. Екатеринбург, ул. Малышева, д. 51', ST_SetSRID(ST_MakePoint(60.6122, 56.8389), 4326), NOW(), NOW()),
        (12, 'г. Екатеринбург, ул. 8 Марта, д. 7', ST_SetSRID(ST_MakePoint(60.5879, 56.8443), 4326), NOW(), NOW()),
        (13, 'г. Казань, ул. Баумана, д. 51', ST_SetSRID(ST_MakePoint(49.1214, 55.7964), 4326), NOW(), NOW()),
        (14, 'г. Казань, ул. Петербургская, д. 57', ST_SetSRID(ST_MakePoint(49.1092, 55.7958), 4326), NOW(), NOW()),
        (15, 'г. Нижний Новгород, ул. Большая Покровская, д. 37', ST_SetSRID(ST_MakePoint(44.0020, 56.3287), 4326), NOW(), NOW())
    """)
    )

    # Insert sample organizations
    op.execute(
        text("""
        INSERT INTO organizations (id, name, building_id, created_at, updated_at) VALUES
        -- Food companies
        (1, 'ООО "Рога и Копыта"', 1, NOW(), NOW()),
        (2, 'ООО "Сырный Рай"', 2, NOW(), NOW()),
        (3, 'АО "Мясной Двор"', 3, NOW(), NOW()),
        (4, 'ООО "Молочный Круг"', 4, NOW(), NOW()),
        (5, 'ИП "Фермерские Продукты"', 5, NOW(), NOW()),
        (6, 'ООО "Колбасный Делюкс"', 6, NOW(), NOW()),
        (7, 'ЗАО "Сыроварня №1"', 7, NOW(), NOW()),
        
        -- Auto companies
        (8, 'ЗАО "Грузовики РФ"', 8, NOW(), NOW()),
        (9, 'ООО "Каршеринг Плюс"', 9, NOW(), NOW()),
        (10, 'ИП "Автозапчасти 24"', 10, NOW(), NOW()),
        (11, 'ООО "Тачка Сервис"', 11, NOW(), NOW()),
        (12, 'ООО "Мотор-Авто"', 12, NOW(), NOW()),
        (13, 'АО "ГрузТрансСервис"', 13, NOW(), NOW()),
        
        -- Education companies
        (14, 'ООО "Школа Развития"', 14, NOW(), NOW()),
        (15, 'АО "Технический Университет"', 15, NOW(), NOW()),
        (16, 'ООО "Курсы IT Pro"', 1, NOW(), NOW()),
        (17, 'ИП "Центр Подготовки"', 2, NOW(), NOW()),
        
        -- Medical companies
        (18, 'ООО "Семейная Стоматология"', 3, NOW(), NOW()),
        (19, 'АО "Хирургический Центр"', 4, NOW(), NOW()),
        (20, 'ООО "Медицинский Центр Здоровье"', 5, NOW(), NOW()),
        (21, 'АО "Фарма Групп"', 6, NOW(), NOW()),
        
        -- Technology companies
        (22, 'ООО "SoftTech Solutions"', 7, NOW(), NOW()),
        (23, 'АО "IT Консалтинг"', 8, NOW(), NOW()),
        (24, 'ООО "Компьютерные Технологии"', 9, NOW(), NOW()),
        (25, 'ИП "Веб-Студия Профессионал"', 10, NOW(), NOW()),
        
        -- Construction companies
        (26, 'ООО "ЖилСтройПроект"', 11, NOW(), NOW()),
        (27, 'АО "ПромСтройСервис"', 12, NOW(), NOW()),
        (28, 'ООО "РемонтМастер"', 13, NOW(), NOW()),
        (29, 'ЗАО "СтройИнвест"', 14, NOW(), NOW())
    """)
    )

    # Insert sample phone numbers - ensuring uniqueness
    op.execute(
        text("""
        INSERT INTO phones (id, number, organization_id, created_at, updated_at) VALUES
        -- Phones for food companies
        (1, '2-222-222', 1, NOW(), NOW()),
        (2, '3-333-333', 1, NOW(), NOW()),
        (3, '8-923-666-13-13', 1, NOW(), NOW()),
        (4, '8-911-123-45-67', 2, NOW(), NOW()),
        (5, '8-987-654-32-10', 3, NOW(), NOW()),
        (6, '8-900-111-22-33', 4, NOW(), NOW()),
        (7, '8-922-444-55-66', 5, NOW(), NOW()),
        (8, '8-901-777-88-99', 6, NOW(), NOW()),
        (9, '8-902-333-44-55', 7, NOW(), NOW()),
        (10, '8-903-555-77-88', 7, NOW(), NOW()),
        
        -- Phones for auto companies
        (11, '8-916-123-45-67', 8, NOW(), NOW()),
        (12, '8-915-987-65-43', 9, NOW(), NOW()),
        (13, '8-926-111-22-33', 10, NOW(), NOW()),
        (14, '8-905-444-55-66', 11, NOW(), NOW()),
        (15, '8-909-777-88-99', 12, NOW(), NOW()),
        (16, '8-910-333-44-55', 13, NOW(), NOW()),
        
        -- Phones for education companies
        (17, '8-911-222-33-44', 14, NOW(), NOW()),
        (18, '8-921-555-66-77', 15, NOW(), NOW()),
        (19, '8-931-888-99-00', 16, NOW(), NOW()),
        (20, '8-901-111-22-33', 17, NOW(), NOW()),
        
        -- Phones for medical companies
        (21, '8-902-333-44-77', 18, NOW(), NOW()),
        (22, '8-903-666-77-88', 19, NOW(), NOW()),
        (23, '8-904-999-00-11', 20, NOW(), NOW()),
        (24, '8-905-222-33-44', 21, NOW(), NOW()),
        
        -- Phones for technology companies
        (25, '8-906-555-66-77', 22, NOW(), NOW()),
        (26, '8-907-888-99-00', 23, NOW(), NOW()),
        (27, '8-908-111-22-33', 24, NOW(), NOW()),
        (28, '8-916-444-55-66', 25, NOW(), NOW()),
        
        -- Phones for construction companies
        (29, '8-917-777-88-99', 26, NOW(), NOW()),
        (30, '8-918-222-33-44', 27, NOW(), NOW()),
        (31, '8-919-555-66-77', 28, NOW(), NOW()),
        (32, '8-925-888-99-00', 29, NOW(), NOW()),
        (33, '8-924-111-22-33', 29, NOW(), NOW())
    """)
    )

    # Link organizations to activities
    op.execute(
        text("""
        INSERT INTO organization_activities (organization_id, activity_id, created_at, updated_at) VALUES
        -- Food companies
        (1, 2, NOW(), NOW()), -- ООО "Рога и Копыта" - Мясная продукция
        (1, 3, NOW(), NOW()), -- ООО "Рога и Копыта" - Молочная продукция
        (2, 3, NOW(), NOW()), -- ООО "Сырный Рай" - Молочная продукция
        (3, 2, NOW(), NOW()), -- АО "Мясной Двор" - Мясная продукция
        (4, 3, NOW(), NOW()), -- ООО "Молочный Круг" - Молочная продукция
        (5, 2, NOW(), NOW()), -- ИП "Фермерские Продукты" - Мясная продукция
        (5, 3, NOW(), NOW()), -- ИП "Фермерские Продукты" - Молочная продукция
        (6, 2, NOW(), NOW()), -- ООО "Колбасный Делюкс" - Мясная продукция
        (7, 3, NOW(), NOW()), -- ЗАО "Сыроварня №1" - Молочная продукция
        
        -- Auto companies
        (8, 5, NOW(), NOW()), -- ЗАО "Грузовики РФ" - Грузовые
        (9, 6, NOW(), NOW()), -- ООО "Каршеринг Плюс" - Легковые
        (10, 7, NOW(), NOW()), -- ИП "Автозапчасти 24" - Запчасти
        (11, 6, NOW(), NOW()), -- ООО "Тачка Сервис" - Легковые
        (11, 7, NOW(), NOW()), -- ООО "Тачка Сервис" - Запчасти
        (12, 6, NOW(), NOW()), -- ООО "Мотор-Авто" - Легковые
        (13, 5, NOW(), NOW()), -- АО "ГрузТрансСервис" - Грузовые
        
        -- Education companies
        (14, 10, NOW(), NOW()), -- ООО "Школа Развития" - Школы
        (15, 11, NOW(), NOW()), -- АО "Технический Университет" - ВУЗы
        (16, 12, NOW(), NOW()), -- ООО "Курсы IT Pro" - Курсы
        (17, 12, NOW(), NOW()), -- ИП "Центр Подготовки" - Курсы
        
        -- Medical companies
        (18, 14, NOW(), NOW()), -- ООО "Семейная Стоматология" - Стоматология
        (19, 15, NOW(), NOW()), -- АО "Хирургический Центр" - Хирургия
        (20, 16, NOW(), NOW()), -- ООО "Медицинский Центр Здоровье" - Терапия
        (21, 17, NOW(), NOW()), -- АО "Фарма Групп" - Фармацевтика
        
        -- Technology companies
        (22, 19, NOW(), NOW()), -- ООО "SoftTech Solutions" - Программирование
        (23, 20, NOW(), NOW()), -- АО "IT Консалтинг" - Консалтинг
        (24, 21, NOW(), NOW()), -- ООО "Компьютерные Технологии" - IT-оборудование
        (25, 19, NOW(), NOW()), -- ИП "Веб-Студия Профессионал" - Программирование
        
        -- Construction companies
        (26, 23, NOW(), NOW()), -- ООО "ЖилСтройПроект" - Жилищное строительство
        (27, 24, NOW(), NOW()), -- АО "ПромСтройСервис" - Промышленное строительство
        (28, 25, NOW(), NOW()), -- ООО "РемонтМастер" - Ремонтные работы
        (29, 22, NOW(), NOW())  -- ЗАО "СтройИнвест" - Строительство
    """)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove organization-activity relationships
    op.execute(
        text(
            "DELETE FROM organization_activities WHERE organization_id BETWEEN 1 AND 29"
        )
    )
    op.execute(text("DELETE FROM phones WHERE organization_id BETWEEN 1 AND 29"))
    op.execute(text("DELETE FROM organizations WHERE id BETWEEN 1 AND 29"))
    op.execute(text("DELETE FROM buildings WHERE id BETWEEN 1 AND 15"))
    op.execute(text("DELETE FROM activities WHERE id BETWEEN 1 AND 25"))
