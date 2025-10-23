"""initial

Revision ID: d06f7f373754
Revises: 
Create Date: 2025-10-23 13:34:43.761804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd06f7f373754'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Сначала создаем таблицу activities с nullable parent_id
    op.create_table('activities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),  # Изменено на nullable=True
    sa.Column('level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['activities.id'], name=op.f('fk_activities_parent_id_activities')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_activities'))
    )
    op.create_index(op.f('ix_activities_id'), 'activities', ['id'], unique=False)
    op.create_index(op.f('ix_activities_name'), 'activities', ['name'], unique=False)

    op.create_table('buildings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_buildings'))
    )
    op.create_index(op.f('ix_buildings_address'), 'buildings', ['address'], unique=False)
    op.create_index(op.f('ix_buildings_id'), 'buildings', ['id'], unique=False)

    op.create_table('organizations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('phone_numbers', sa.ARRAY(sa.String(length=20)), nullable=False),
    sa.Column('building_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], name=op.f('fk_organizations_building_id_buildings')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_organizations')),
    sa.UniqueConstraint('name', name=op.f('uq_organizations_name'))
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)

    op.create_table('organization_activity',
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name=op.f('fk_organization_activity_activity_id_activities')),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name=op.f('fk_organization_activity_organization_id_organizations'))
    )

    # Вставка тестовых данных
    op.bulk_insert(
        sa.table('buildings',
            sa.column('id', sa.Integer),
            sa.column('address', sa.String),
            sa.column('latitude', sa.Float),
            sa.column('longitude', sa.Float)
        ),
        [
            {'id': 1, 'address': 'ул. Ленина, 25', 'latitude': 55.7558, 'longitude': 37.6173},
            {'id': 2, 'address': 'пр. Мира, 15', 'latitude': 55.7604, 'longitude': 37.6185},
            {'id': 3, 'address': 'ул. Пушкина, 10', 'latitude': 55.7500, 'longitude': 37.6000},
            {'id': 4, 'address': 'ул. Гагарина, 5', 'latitude': 55.7654, 'longitude': 37.6211},
            {'id': 5, 'address': 'ул. Садовая, 30', 'latitude': 55.7522, 'longitude': 37.6155},
        ]
    )

    # Сначала вставляем корневые элементы (уровень 1) без parent_id
    op.bulk_insert(
        sa.table('activities',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('parent_id', sa.Integer),
                 sa.column('level', sa.Integer)
                 ),
        [
            # Уровень 1 - Основные категории (parent_id = NULL)
            {'id': 1, 'name': 'Образование', 'parent_id': None, 'level': 1},
            {'id': 2, 'name': 'Медицина', 'parent_id': None, 'level': 1},
            {'id': 3, 'name': 'Торговля', 'parent_id': None, 'level': 1},
            {'id': 4, 'name': 'Услуги', 'parent_id': None, 'level': 1},
        ]
    )

    # Затем вставляем остальные уровни
    op.bulk_insert(
        sa.table('activities',
                 sa.column('id', sa.Integer),
                 sa.column('name', sa.String),
                 sa.column('parent_id', sa.Integer),
                 sa.column('level', sa.Integer)
                 ),
        [
            # Уровень 2 - Подкатегории образования
            {'id': 5, 'name': 'Школы', 'parent_id': 1, 'level': 2},
            {'id': 6, 'name': 'Вузы', 'parent_id': 1, 'level': 2},
            {'id': 7, 'name': 'Детские сады', 'parent_id': 1, 'level': 2},

            # Уровень 2 - Подкатегории медицины
            {'id': 8, 'name': 'Поликлиники', 'parent_id': 2, 'level': 2},
            {'id': 9, 'name': 'Больницы', 'parent_id': 2, 'level': 2},
            {'id': 10, 'name': 'Стоматологии', 'parent_id': 2, 'level': 2},

            # Уровень 2 - Подкатегории торговли
            {'id': 11, 'name': 'Продуктовые магазины', 'parent_id': 3, 'level': 2},
            {'id': 12, 'name': 'Одежда и обувь', 'parent_id': 3, 'level': 2},
            {'id': 13, 'name': 'Электроника', 'parent_id': 3, 'level': 2},

            # Уровень 2 - Подкатегории услуг
            {'id': 14, 'name': 'Парикмахерские', 'parent_id': 4, 'level': 2},
            {'id': 15, 'name': 'Ремонт техники', 'parent_id': 4, 'level': 2},
            {'id': 16, 'name': 'Юридические услуги', 'parent_id': 4, 'level': 2},

            # Уровень 3 - Конкретные виды деятельности
            {'id': 17, 'name': 'Средняя общеобразовательная школа', 'parent_id': 5, 'level': 3},
            {'id': 18, 'name': 'Гимназия', 'parent_id': 5, 'level': 3},
            {'id': 19, 'name': 'Лицей', 'parent_id': 5, 'level': 3},

            {'id': 20, 'name': 'Университет', 'parent_id': 6, 'level': 3},
            {'id': 21, 'name': 'Институт', 'parent_id': 6, 'level': 3},
            {'id': 22, 'name': 'Академия', 'parent_id': 6, 'level': 3},

            {'id': 23, 'name': 'Детская поликлиника', 'parent_id': 8, 'level': 3},
            {'id': 24, 'name': 'Взрослая поликлиника', 'parent_id': 8, 'level': 3},
            {'id': 25, 'name': 'Стоматологическая клиника', 'parent_id': 10, 'level': 3},

            {'id': 26, 'name': 'Супермаркет', 'parent_id': 11, 'level': 3},
            {'id': 27, 'name': 'Продуктовый магазин у дома', 'parent_id': 11, 'level': 3},
        ]
    )

    op.bulk_insert(
        sa.table('organizations',
                 sa.column('id', sa.Integer),
                 sa.column('name', sa.String),
                 sa.column('phone_numbers', sa.ARRAY(sa.String)),
                 sa.column('building_id', sa.Integer)
                 ),
        [
            {'id': 1, 'name': 'Школа №1', 'phone_numbers': ['+7(495)123-45-67', '+7(495)123-45-68'], 'building_id': 1},
            {'id': 2, 'name': 'МГУ им. Ломоносова', 'phone_numbers': ['+7(495)939-10-00'], 'building_id': 2},
            {'id': 3, 'name': 'Детский сад "Солнышко"', 'phone_numbers': ['+7(495)234-56-78'], 'building_id': 3},
            {'id': 4, 'name': 'Городская поликлиника №5', 'phone_numbers': ['+7(495)345-67-89', '+7(495)345-67-90'],
             'building_id': 4},
            {'id': 5, 'name': 'Стоматология "Улыбка"', 'phone_numbers': ['+7(495)456-78-90'], 'building_id': 5},
            {'id': 6, 'name': 'Супермаркет "Продукты"', 'phone_numbers': ['+7(495)567-89-01'], 'building_id': 1},
            {'id': 7, 'name': 'Магазин одежды "Стиль"', 'phone_numbers': ['+7(495)678-90-12'], 'building_id': 2},
            {'id': 8, 'name': 'Парикмахерская "Элегант"', 'phone_numbers': ['+7(495)789-01-23'], 'building_id': 3},
            {'id': 9, 'name': 'Лицей информационных технологий', 'phone_numbers': ['+7(495)890-12-34'],
             'building_id': 4},
            {'id': 10, 'name': 'Юридическая фирма "Право"', 'phone_numbers': ['+7(495)901-23-45'], 'building_id': 5},
        ]
    )

    # Связи организаций с видами деятельности
    op.bulk_insert(
        sa.table('organization_activity',
                 sa.column('organization_id', sa.Integer),
                 sa.column('activity_id', sa.Integer)
                 ),
        [
            # Школа №1 связана с несколькими видами деятельности
            {'organization_id': 1, 'activity_id': 17},  # Средняя общеобразовательная школа
            {'organization_id': 1, 'activity_id': 18},  # Гимназия

            # МГУ - университет
            {'organization_id': 2, 'activity_id': 20},  # Университет

            # Детский сад
            {'organization_id': 3, 'activity_id': 7},  # Детские сады

            # Поликлиника
            {'organization_id': 4, 'activity_id': 23},  # Детская поликлиника
            {'organization_id': 4, 'activity_id': 24},  # Взрослая поликлиника

            # Стоматология
            {'organization_id': 5, 'activity_id': 25},  # Стоматологическая клиника

            # Супермаркет
            {'organization_id': 6, 'activity_id': 26},  # Супермаркет

            # Магазин одежды
            {'organization_id': 7, 'activity_id': 12},  # Одежда и обувь

            # Парикмахерская
            {'organization_id': 8, 'activity_id': 14},  # Парикмахерские

            # Лицей
            {'organization_id': 9, 'activity_id': 19},  # Лицей

            # Юридическая фирма
            {'organization_id': 10, 'activity_id': 16},  # Юридические услуги
        ]
    )


def downgrade() -> None:
    # Сначала удаляем данные из связующих таблиц
    op.execute("DELETE FROM organization_activity")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM activities")
    op.execute("DELETE FROM buildings")

    # Затем удаляем таблицы
    op.drop_table('organization_activity')
    op.drop_index(op.f('ix_organizations_id'), table_name='organizations')
    op.drop_table('organizations')
    op.drop_index(op.f('ix_buildings_id'), table_name='buildings')
    op.drop_index(op.f('ix_buildings_address'), table_name='buildings')
    op.drop_table('buildings')
    op.drop_index(op.f('ix_activities_name'), table_name='activities')
    op.drop_index(op.f('ix_activities_id'), table_name='activities')
    op.drop_table('activities')

