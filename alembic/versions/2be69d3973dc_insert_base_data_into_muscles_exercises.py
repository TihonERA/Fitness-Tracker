"""Insert base data into muscles & exercises

Revision ID: 2be69d3973dc
Revises: 70cb075bf6c0
Create Date: 2026-07-03 16:15:14.457152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import json


# revision identifiers, used by Alembic.
revision: str = '2be69d3973dc'
down_revision: Union[str, Sequence[str], None] = '70cb075bf6c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    op.create_table(
        'muscle',
        sa.Column('muscle_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        if_not_exists=True
    )

    op.create_index('ix_muscle_name', 'muscle', ['name'], if_not_exists=True)
    
    op.create_table(
        'exercise',
        sa.Column('exercise_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('gif_url', sa.Text(), nullable=True),
        sa.Column('muscle_activation', sa.JSON(), server_default='{}', nullable=False),
        if_not_exists=True
    )

    muscles = sa.table('muscle', sa.column('name'))
    exercises = sa.table(
        'exercise',
        sa.column('name'),
        sa.column('description'),
        sa.column('gif_url'),
        sa.column('muscle_activation')
    )

    conn.execute(
        sa.insert(muscles),
        [
            {"name": "chest"},
            {"name": "upper_back"},
            {"name": "lower_back"},
            {"name": "shoulders"},
            {"name": "traps"},
            {"name": "biceps"},
            {"name": "triceps"},
            {"name": "forearms"},
            {"name": "hips"},
            {"name": "abs"},
            {"name": "obliques"},
            {"name": "quads"},
            {"name": "hamstrings"},
            {"name": "glutes"},
            {"name": "calves"},
        ]
    )

    conn.execute(
        sa.insert(exercises),
        [
            {
                "name": "bench press (flat)",
                "description": "Классический жим лёжа на горизонтальной скамье. Основное упражнение для развития груди, также нагружает трицепс и передние дельты.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.60, "triceps": 0.25, "shoulders": 0.15})
            },
            {
                "name": "bench press (incline)",
                "description": "Жим на наклонной скамье (головой вверх). Акцент на верхнюю часть груди и передние дельты.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.50, "shoulders": 0.30, "triceps": 0.20})
            },
            {
                "name": "dumbbell press",
                "description": "Жим гантелей лёжа на горизонтальной скамье. Позволяет большую амплитуду и симметричную нагрузку на грудь.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.55, "triceps": 0.25, "shoulders": 0.20})
            },
            {
                "name": "dumbbell flyes",
                "description": "Разводка гантелей лёжа. Изолирующее упражнение для грудных мышц, работа в приводящей фазе.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.80, "shoulders": 0.15, "triceps": 0.05})
            },
            {
                "name": "push-ups",
                "description": "Отжимания от пола. Базовое упражнение с собственным весом, задействует грудь, трицепс и передние дельты.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.55, "triceps": 0.30, "shoulders": 0.15})
            },
            {
                "name": "dips",
                "description": "Отжимания на брусьях. Мощное упражнение для нижней части груди и трицепсов.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.50, "triceps": 0.40, "shoulders": 0.10})
            },
            {
                "name": "cable flyes",
                "description": "Сведение рук в кроссовере. Постоянное напряжение на протяжении всего движения, хорошо изолирует грудь.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.75, "shoulders": 0.15, "triceps": 0.10})
            },
            {
                "name": "chest press machine",
                "description": "Жим в тренажёре для груди. Стабильная траектория, безопасная альтернатива свободным весам.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.65, "triceps": 0.20, "shoulders": 0.15})
            },
            {
                "name": "pull-ups",
                "description": "Подтягивания на перекладине. Базовое упражнение для широчайших и верхней части спины.",
                "gif_url": None,
                "muscle_activation": json.dumps({"upper_back": 0.70, "biceps": 0.20, "shoulders": 0.10})
            },
            {
                "name": "barbell row",
                "description": "Тяга штанги в наклоне. Массонаборное упражнение для средней и верхней части спины.",
                "gif_url": None,
                "muscle_activation": json.dumps({"upper_back": 0.65, "biceps": 0.20, "shoulders": 0.15})
            },
            {
                "name": "one-arm dumbbell row",
                "description": "Тяга гантели одной рукой в наклоне. Хорошо прорабатывает широчайшие с акцентом на каждую сторону.",
                "gif_url": None,
                "muscle_activation": json.dumps({"upper_back": 0.70, "biceps": 0.20, "shoulders": 0.10})
            },
            {
                "name": "lat pulldown",
                "description": "Тяга верхнего блока к груди. Заменяет подтягивания, отлично развивает широчайшие.",
                "gif_url": None,
                "muscle_activation": json.dumps({"upper_back": 0.75, "biceps": 0.15, "shoulders": 0.10})
            },
            {
                "name": "seated cable row",
                "description": "Тяга блока сидя к животу. Работает на толщину спины, включает ромбовидные и трапеции.",
                "gif_url": None,
                "muscle_activation": json.dumps({"upper_back": 0.70, "biceps": 0.15, "shoulders": 0.10, "traps": 0.05})
            },
            {
                "name": "t-bar row",
                "description": "Тяга Т-грифа. Мощное базовое движение для средней части спины.",
                "gif_url": None,
                "muscle_activation": json.dumps({"upper_back": 0.70, "biceps": 0.15, "shoulders": 0.10, "traps": 0.05})
            },
            {
                "name": "dumbbell pullover",
                "description": "Пуловер с гантелью лёжа. Растягивает грудную клетку и включает широчайшие.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.40, "upper_back": 0.40, "triceps": 0.20})
            },
            {
                "name": "deadlift",
                "description": "Классическая становая тяга. Задействует всё тело, особенно спину, ягодицы и заднюю поверхность бедра.",
                "gif_url": None,
                "muscle_activation": json.dumps({"lower_back": 0.30, "glutes": 0.25, "hamstrings": 0.20, "upper_back": 0.15, "quads": 0.10})
            },
            {
                "name": "romanian deadlift",
                "description": "Румынская тяга на прямых ногах. Акцент на бицепс бедра и ягодицы.",
                "gif_url": None,
                "muscle_activation": json.dumps({"hamstrings": 0.45, "glutes": 0.30, "lower_back": 0.25})
            },
            {
                "name": "hyperextension",
                "description": "Гиперэкстензия на римском стуле. Изолирует разгибатели позвоночника.",
                "gif_url": None,
                "muscle_activation": json.dumps({"lower_back": 0.70, "glutes": 0.20, "hamstrings": 0.10})
            },
            {
                "name": "good mornings",
                "description": "Наклоны со штангой на плечах. Прорабатывает поясницу и заднюю цепь.",
                "gif_url": None,
                "muscle_activation": json.dumps({"lower_back": 0.50, "hamstrings": 0.30, "glutes": 0.20})
            },
            {
                "name": "overhead press",
                "description": "Жим штанги стоя (армейский). Базовое упражнение для дельт, особенно переднего и среднего пучков.",
                "gif_url": None,
                "muscle_activation": json.dumps({"shoulders": 0.60, "triceps": 0.25, "traps": 0.15})
            },
            {
                "name": "seated dumbbell press",
                "description": "Жим гантелей сидя. Безопаснее для поясницы, хорошо нагружает все пучки дельт.",
                "gif_url": None,
                "muscle_activation": json.dumps({"shoulders": 0.60, "triceps": 0.25, "traps": 0.15})
            },
            {
                "name": "lateral raises",
                "description": "Разведение гантелей в стороны. Изолирующее упражнение на средний пучок дельт.",
                "gif_url": None,
                "muscle_activation": json.dumps({"shoulders": 0.80, "traps": 0.15, "forearms": 0.05})
            },
            {
                "name": "rear delt flyes",
                "description": "Разведение гантелей в наклоне или на блоке. Целевая нагрузка на задний пучок дельт.",
                "gif_url": None,
                "muscle_activation": json.dumps({"shoulders": 0.70, "upper_back": 0.20, "traps": 0.10})
            },
            {
                "name": "upright row",
                "description": "Тяга штанги к подбородку. Развивает трапеции и средние дельты.",
                "gif_url": None,
                "muscle_activation": json.dumps({"traps": 0.40, "shoulders": 0.40, "biceps": 0.20})
            },
            {
                "name": "arnold press",
                "description": "Жим Арнольда с поворотом кистей. Включает все пучки дельт за счёт ротации.",
                "gif_url": None,
                "muscle_activation": json.dumps({"shoulders": 0.65, "triceps": 0.20, "traps": 0.15})
            },
            {
                "name": "barbell shrugs",
                "description": "Шраги со штангой. Основное упражнение для трапециевидных мышц.",
                "gif_url": None,
                "muscle_activation": json.dumps({"traps": 0.80, "shoulders": 0.15, "forearms": 0.05})
            },
            {
                "name": "dumbbell shrugs",
                "description": "Шраги с гантелями. Альтернатива штанге с большей амплитудой.",
                "gif_url": None,
                "muscle_activation": json.dumps({"traps": 0.80, "shoulders": 0.15, "forearms": 0.05})
            },
            {
                "name": "lee haney shrugs",
                "description": "Шраги с паузой в верхней точке и небольшим поворотом плеч. Максимальное сокращение трапеций.",
                "gif_url": None,
                "muscle_activation": json.dumps({"traps": 0.85, "shoulders": 0.10, "forearms": 0.05})
            },
            {
                "name": "barbell curl",
                "description": "Подъём штанги на бицепс стоя. Базовое упражнение для двуглавой мышцы плеча.",
                "gif_url": None,
                "muscle_activation": json.dumps({"biceps": 0.80, "forearms": 0.15, "shoulders": 0.05})
            },
            {
                "name": "hammer curl",
                "description": "Молотковые сгибания с гантелями (нейтральный хват). Акцент на брахиалис и плечевую мышцу.",
                "gif_url": None,
                "muscle_activation": json.dumps({"biceps": 0.70, "forearms": 0.25, "shoulders": 0.05})
            },
            {
                "name": "dumbbell curl",
                "description": "Поочерёдный или одновременный подъём гантелей на бицепс. Хорошо прорабатывает пик бицепса.",
                "gif_url": None,
                "muscle_activation": json.dumps({"biceps": 0.80, "forearms": 0.15, "shoulders": 0.05})
            },
            {
                "name": "preacher curl",
                "description": "Сгибание рук на скамье Скотта. Изолирует бицепс, исключая читинг.",
                "gif_url": None,
                "muscle_activation": json.dumps({"biceps": 0.85, "forearms": 0.10, "shoulders": 0.05})
            },
            {
                "name": "concentration curl",
                "description": "Концентрированный подъём гантели на бицепс с опорой локтя о колено. Максимальная пиковая нагрузка.",
                "gif_url": None,
                "muscle_activation": json.dumps({"biceps": 0.85, "forearms": 0.10, "shoulders": 0.05})
            },
            {
                "name": "skull crushers",
                "description": "Разгибание рук лёжа (французский жим) с EZ-грифом. Изолирует трицепс.",
                "gif_url": None,
                "muscle_activation": json.dumps({"triceps": 0.85, "chest": 0.10, "shoulders": 0.05})
            },
            {
                "name": "french press",
                "description": "Французский жим стоя или сидя с одной гантелью. Нагрузка на длинную головку трицепса.",
                "gif_url": None,
                "muscle_activation": json.dumps({"triceps": 0.85, "shoulders": 0.10, "chest": 0.05})
            },
            {
                "name": "tricep pushdown (rope)",
                "description": "Разгибание рук на блоке с канатной рукоятью. Пик сокращения и проработка боковой головки.",
                "gif_url": None,
                "muscle_activation": json.dumps({"triceps": 0.90, "shoulders": 0.05, "forearms": 0.05})
            },
            {
                "name": "tricep pushdown (bar)",
                "description": "Разгибание рук на блоке с прямой рукоятью. Базовая изоляция трицепса.",
                "gif_url": None,
                "muscle_activation": json.dumps({"triceps": 0.90, "shoulders": 0.05, "forearms": 0.05})
            },
            {
                "name": "bench dips",
                "description": "Обратные отжимания между скамьями. Работают трицепс и передние дельты.",
                "gif_url": None,
                "muscle_activation": json.dumps({"triceps": 0.60, "shoulders": 0.25, "chest": 0.15})
            },
            {
                "name": "close-grip bench press",
                "description": "Жим лёжа узким хватом. Смещает акцент на трицепсы, сохраняя нагрузку на грудь.",
                "gif_url": None,
                "muscle_activation": json.dumps({"triceps": 0.50, "chest": 0.30, "shoulders": 0.20})
            },
            {
                "name": "wrist curls",
                "description": "Сгибание кистей со штангой (сидя, предплечья на скамье). Развивает внутреннюю группу мышц предплечья.",
                "gif_url": None,
                "muscle_activation": json.dumps({"forearms": 0.90, "biceps": 0.05, "shoulders": 0.05})
            },
            {
                "name": "wrist extensions",
                "description": "Разгибание кистей со штангой или гантелями. Противоположное движение, на внешнюю часть предплечья.",
                "gif_url": None,
                "muscle_activation": json.dumps({"forearms": 0.90, "biceps": 0.05, "shoulders": 0.05})
            },
            {
                "name": "crunches",
                "description": "Обычные скручивания лёжа на полу. Базовое упражнение для верхней части пресса.",
                "gif_url": None,
                "muscle_activation": json.dumps({"abs": 0.80, "obliques": 0.15, "hips": 0.05})
            },
            {
                "name": "hanging leg raises",
                "description": "Подъём ног в висе на перекладине. Мощно прорабатывает нижний отдел пресса и мышцы-сгибатели бедра.",
                "gif_url": None,
                "muscle_activation": json.dumps({"abs": 0.70, "obliques": 0.20, "quads": 0.10})
            },
            {
                "name": "roman chair sit-ups",
                "description": "Подъём корпуса на римском стуле. Акцент на прямую мышцу живота с растяжением.",
                "gif_url": None,
                "muscle_activation": json.dumps({"abs": 0.75, "obliques": 0.15, "hips": 0.10})
            },
            {
                "name": "plank",
                "description": "Статическая планка на локтях. Включает весь корсет мышц, особенно прямые и поперечные мышцы живота.",
                "gif_url": None,
                "muscle_activation": json.dumps({"abs": 0.70, "shoulders": 0.15, "lower_back": 0.10, "glutes": 0.05})
            },
            {
                "name": "cable crunches",
                "description": "Скручивания на блоке стоя на коленях. Позволяет добавлять вес для гипертрофии пресса.",
                "gif_url": None,
                "muscle_activation": json.dumps({"abs": 0.80, "obliques": 0.15, "hips": 0.05})
            },
            {
                "name": "barbell squats",
                "description": "Приседания со штангой на плечах. Королевское упражнение для ног и ягодиц.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.40, "glutes": 0.25, "hamstrings": 0.15, "lower_back": 0.10, "abs": 0.10})
            },
            {
                "name": "smith machine squats",
                "description": "Приседания в тренажёре Смита. Снижает нагрузку на стабилизаторы, акцент на квадрицепс.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.45, "glutes": 0.25, "hamstrings": 0.15, "lower_back": 0.10, "abs": 0.05})
            },
            {
                "name": "front squats",
                "description": "Фронтальные приседания с грифом на груди. Смещают нагрузку на квадрицепсы и верхнюю часть спины.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.55, "glutes": 0.15, "hamstrings": 0.10, "upper_back": 0.10, "abs": 0.10})
            },
            {
                "name": "leg press",
                "description": "Жим ногами в платформенном тренажёре. Менее травматичная альтернатива приседаниям.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.50, "glutes": 0.25, "hamstrings": 0.20, "calves": 0.05})
            },
            {
                "name": "leg extensions",
                "description": "Разгибание ног в тренажёре. Изолирующее упражнение на квадрицепс.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.85, "glutes": 0.05, "hamstrings": 0.10})
            },
            {
                "name": "lunges",
                "description": "Выпады со штангой или гантелями. Отлично нагружают ягодицы и квадрицепс, улучшают баланс.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.40, "glutes": 0.30, "hamstrings": 0.20, "abs": 0.10})
            },
            {
                "name": "hack squats",
                "description": "Приседания в тренажёре хаккеншмидта. Акцент на наружную часть квадрицепса.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.60, "glutes": 0.20, "hamstrings": 0.15, "calves": 0.05})
            },
            {
                "name": "lying leg curls",
                "description": "Сгибание ног лёжа в тренажёре. Изолирует бицепс бедра.",
                "gif_url": None,
                "muscle_activation": json.dumps({"hamstrings": 0.90, "glutes": 0.05, "calves": 0.05})
            },
            {
                "name": "seated leg curls",
                "description": "Сгибание ног сидя. Нагружает внутреннюю часть задней поверхности бедра.",
                "gif_url": None,
                "muscle_activation": json.dumps({"hamstrings": 0.90, "glutes": 0.05, "calves": 0.05})
            },
            {
                "name": "glute bridge",
                "description": "Ягодичный мостик лёжа на полу. Основное изолирующее упражнение для ягодиц.",
                "gif_url": None,
                "muscle_activation": json.dumps({"glutes": 0.70, "hamstrings": 0.20, "lower_back": 0.10})
            },
            {
                "name": "cable kickbacks",
                "description": "Махи ногой назад на блоке. Отличная изоляция ягодичных мышц.",
                "gif_url": None,
                "muscle_activation": json.dumps({"glutes": 0.75, "hamstrings": 0.15, "lower_back": 0.10})
            },
            {
                "name": "bulgarian split squats",
                "description": "Болгарские выпады со штангой или гантелями. Сильная нагрузка на ягодицу и квадрицепс передней ноги.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.40, "glutes": 0.35, "hamstrings": 0.15, "abs": 0.10})
            },
            {
                "name": "standing calf raises",
                "description": "Подъём на носки стоя. Базовое упражнение для икроножных мышц (гастронемиус).",
                "gif_url": None,
                "muscle_activation": json.dumps({"calves": 0.85, "quads": 0.10, "glutes": 0.05})
            },
            {
                "name": "seated calf raises",
                "description": "Подъём на носки сидя. Нагружает камбаловидную мышцу под икрой.",
                "gif_url": None,
                "muscle_activation": json.dumps({"calves": 0.90, "hamstrings": 0.05, "quads": 0.05})
            },
            {
                "name": "donkey calf raises",
                "description": "Подъём на носки в наклоне (ослик). Отличный вариант для общего объёма икр.",
                "gif_url": None,
                "muscle_activation": json.dumps({"calves": 0.85, "hamstrings": 0.10, "glutes": 0.05})
            },
            {
                "name": "box jumps",
                "description": "Запрыгивания на тумбу. Взрывное упражнение для ног и ягодиц.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.40, "glutes": 0.30, "calves": 0.20, "hamstrings": 0.10})
            },
            {
                "name": "burpees",
                "description": "Бёрпи — комбинация приседа, отжимания и прыжка. Полнофункциональное упражнение на всё тело.",
                "gif_url": None,
                "muscle_activation": json.dumps({"chest": 0.15, "quads": 0.25, "glutes": 0.15, "shoulders": 0.15, "triceps": 0.10, "abs": 0.10, "calves": 0.10})
            },
            {
                "name": "jump squats",
                "description": "Приседания с прыжком. Развивает взрывную силу ног и кардио.",
                "gif_url": None,
                "muscle_activation": json.dumps({"quads": 0.45, "glutes": 0.25, "calves": 0.20, "hamstrings": 0.10})
            },
            {
                "name": "jump rope",
                "description": "Прыжки через скакалку. Отличное кардио с акцентом на икры и стабилизацию.",
                "gif_url": None,
                "muscle_activation": json.dumps({"calves": 0.60, "quads": 0.15, "glutes": 0.10, "abs": 0.10, "shoulders": 0.05})
            }
        ]                 
    )

def downgrade() -> None:
    pass
