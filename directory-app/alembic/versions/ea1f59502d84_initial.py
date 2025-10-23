"""initial

Revision ID: ea1f59502d84
Revises:
Create Date: 2025-10-23 21:37:45.128476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'ea1f59502d84'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('activities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['activities.id'],
                            name=op.f('fk_activities_parent_id_activities')),
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
    sa.ForeignKeyConstraint(['building_id'], ['buildings.id'],
                            name=op.f('fk_organizations_building_id_buildings')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_organizations')),
    sa.UniqueConstraint('name', name=op.f('uq_organizations_name'))
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)
    op.create_table('organizations_activities',
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'],
                            name=op.f('fk_organizations_activities_activity_id_activities')),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'],
                            name=op.f('fk_organizations_activities_organization_id_organizations')),
    sa.PrimaryKeyConstraint('organization_id', 'activity_id', name=op.f('pk_organizations_activities'))
    )

    # Добавляем тестовые данные
    insert_test_data()


def insert_test_data() -> None:
    # Вставляем здания
    buildings_table = sa.table('buildings',
        sa.column('id', sa.Integer),
        sa.column('address', sa.String),
        sa.column('latitude', sa.Float),
        sa.column('longitude', sa.Float)
    )

    op.bulk_insert(buildings_table, [
        {
            'id': 1,
            'address': 'ул. Ленина, д. 10',
            'latitude': 55.7558,
            'longitude': 37.6173
        },
        {
            'id': 2,
            'address': 'пр. Мира, д. 25',
            'latitude': 55.7604,
            'longitude': 37.6185
        },
        {
            'id': 3,
            'address': 'ул. Пушкина, д. 15',
            'latitude': 55.7500,
            'longitude': 37.6000
        },
        {
            'id': 4,
            'address': 'ул. Гагарина, д. 42',
            'latitude': 55.7700,
            'longitude': 37.6300
        },
        {
            'id': 5,
            'address': 'пр. Ленинградский, д. 8',
            'latitude': 55.7900,
            'longitude': 37.5500
        }
    ])

    # Вставляем виды деятельности (иерархическая структура)
    activities_table = sa.table('activities',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('parent_id', sa.Integer),
        sa.column('level', sa.Integer)
    )

    op.bulk_insert(activities_table, [
        # Уровень 1 - основные категории
        {'id': 1, 'name': 'Образование', 'parent_id': None, 'level': 1},
        {'id': 2, 'name': 'Медицина', 'parent_id': None, 'level': 1},
        {'id': 3, 'name': 'Торговля', 'parent_id': None, 'level': 1},
        {'id': 4, 'name': 'Спорт', 'parent_id': None, 'level': 1},

        # Уровень 2 - подкатегории образования
        {'id': 5, 'name': 'Школы', 'parent_id': 1, 'level': 2},
        {'id': 6, 'name': 'Вузы', 'parent_id': 1, 'level': 2},
        {'id': 7, 'name': 'Курсы', 'parent_id': 1, 'level': 2},

        # Уровень 2 - подкатегории медицины
        {'id': 8, 'name': 'Поликлиники', 'parent_id': 2, 'level': 2},
        {'id': 9, 'name': 'Больницы', 'parent_id': 2, 'level': 2},
        {'id': 10, 'name': 'Стоматология', 'parent_id': 2, 'level': 2},

        # Уровень 2 - подкатегории торговли
        {'id': 11, 'name': 'Продуктовые магазины', 'parent_id': 3, 'level': 2},
        {'id': 12, 'name': 'Одежда', 'parent_id': 3, 'level': 2},
        {'id': 13, 'name': 'Электроника', 'parent_id': 3, 'level': 2},

        # Уровень 2 - подкатегории спорта
        {'id': 14, 'name': 'Фитнес-клубы', 'parent_id': 4, 'level': 2},
        {'id': 15, 'name': 'Бассейны', 'parent_id': 4, 'level': 2},
        {'id': 16, 'name': 'Спортивные секции', 'parent_id': 4, 'level': 2}
    ])

    # Вставляем организации
    organizations_table = sa.table('organizations',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('phone_numbers', sa.ARRAY(sa.String)),
        sa.column('building_id', sa.Integer)
    )

    op.bulk_insert(organizations_table, [
        {
            'id': 1,
            'name': 'Средняя школа №1',
            'phone_numbers': ['+7(495)111-11-11', '+7(495)111-11-12'],
            'building_id': 1
        },
        {
            'id': 2,
            'name': 'Городская больница',
            'phone_numbers': ['+7(495)222-22-22'],
            'building_id': 2
        },
        {
            'id': 3,
            'name': 'Супермаркет "Продукты"',
            'phone_numbers': ['+7(495)333-33-33'],
            'building_id': 3
        },
        {
            'id': 4,
            'name': 'Фитнес-центр "СпортЛайф"',
            'phone_numbers': ['+7(495)444-44-44', '+7(495)444-44-45'],
            'building_id': 4
        },
        {
            'id': 5,
            'name': 'Университет им. Ломоносова',
            'phone_numbers': ['+7(495)555-55-55'],
            'building_id': 5
        },
        {
            'id': 6,
            'name': 'Стоматология "Улыбка"',
            'phone_numbers': ['+7(495)666-66-66'],
            'building_id': 1
        },
        {
            'id': 7,
            'name': 'Магазин электроники "Техномир"',
            'phone_numbers': ['+7(495)777-77-77'],
            'building_id': 2
        }
    ])

    # Вставляем связи организаций с видами деятельности
    org_activities_table = sa.table('organizations_activities',
        sa.column('organization_id', sa.Integer),
        sa.column('activity_id', sa.Integer)
    )

    op.bulk_insert(org_activities_table, [
        # Школа
        {'organization_id': 1, 'activity_id': 1},  # Образование
        {'organization_id': 1, 'activity_id': 5},  # Школы

        # Больница
        {'organization_id': 2, 'activity_id': 2},  # Медицина
        {'organization_id': 2, 'activity_id': 9},  # Больницы

        # Супермаркет
        {'organization_id': 3, 'activity_id': 3},  # Торговля
        {'organization_id': 3, 'activity_id': 11},  # Продуктовые магазины

        # Фитнес-центр
        {'organization_id': 4, 'activity_id': 4},  # Спорт
        {'organization_id': 4, 'activity_id': 14},  # Фитнес-клубы
        {'organization_id': 4, 'activity_id': 15},  # Бассейны

    # Университет
        {'organization_id': 5, 'activity_id': 1},  # Образование
        {'organization_id': 5, 'activity_id': 6},  # Вузы

        # Стоматология
        {'organization_id': 6, 'activity_id': 2},  # Медицина
        {'organization_id': 6, 'activity_id': 10},  # Стоматология

        # Магазин электроники
        {'organization_id': 7, 'activity_id': 3},  # Торговля
        {'organization_id': 7, 'activity_id': 13}  # Электроника
    ])

def downgrade() -> None:
    # Удаляем тестовые данные (опционально, можно оставить пустым)
    op.execute("DELETE FROM organizations_activities")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM activities")
    op.execute("DELETE FROM buildings")
    op.drop_table('organizations_activities')
    op.drop_index(op.f('ix_organizations_id'), table_name='organizations')
    op.drop_table('organizations')
    op.drop_index(op.f('ix_buildings_id'), table_name='buildings')
    op.drop_index(op.f('ix_buildings_address'), table_name='buildings')
    op.drop_table('buildings')
    op.drop_index(op.f('ix_activities_name'), table_name='activities')
    op.drop_index(op.f('ix_activities_id'), table_name='activities')
    op.drop_table('activities')