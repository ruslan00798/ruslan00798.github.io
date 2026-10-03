# ==========================
# profile_service.py
#
# Логика профиля пользователя
# ==========================
import logging

from dataclasses import dataclass

from utils.level import calculate_level
from utils.achievements import get_achievements

logger = logging.getLogger(__name__)

@dataclass
class ProfileData:
    language: str | None

    xp: int

    level: dict

    translations: int

    favorites: int

    learned_words: int

    goal_progress: int

    goal_target: int

    achievements: list


class ProfileService:

    def __init__(self, repository):
        self.repository = repository

    async def get_profile_data(
        self,
        user_id: int
    ) -> ProfileData:
        """
        Собирает все данные профиля.
        """

        logger.info(
            "начало получения профиля: user_id=%s",
            user_id,
        )

        try:
            stats = await self.repository.get_statistics(
                user_id
            )

            xp = await self.repository.get_xp(
                user_id
            )

            learned = await self.repository.get_learned_words(
                user_id
            )

            language = await self.repository.get_language(
                user_id
            )

            goal = await self.repository.get_daily_goal(
                user_id
            )

        except Exception:
            logger.exception(
                "ошибка при получении данных профиля: user_id=%s",
                user_id,
            )
            raise
        # ==========================
        # Нормализация типов
        # ==========================

        try:
            xp = int(xp)
        except (TypeError, ValueError):
            logger.warning(
                "некорректное значение XP, установлено 0: user_id=%s value=%r",
                user_id,
                xp,
            )
            xp = 0

        try:
            learned = int(learned)
        except (TypeError, ValueError):
            logger.warning(
                "некорректное количество изученных слов,"
                "установлено 0: user_id=%s, value=%s",
                user_id,
                learned
            )
            learned = 0

        translations = int(
            stats.get("translations", 0)
        )

        favorites = int(
            stats.get("favorites", 0)
        )

        level = calculate_level(xp)

        achievements = get_achievements(
            translations,
            xp,
            learned,
        )

        # ==========================
        # Цель дня
        # ==========================

        if goal:

            progress = int(goal.get("completed", 0))

            target = int(goal.get("target", 10))

        else:

            progress = 0
            target = 10

        logger.info(
            "Профиль собран:"
            "user_id=%s, xp=%s, level=%s,"
            "translations=%s, favorites=%s,"
            "learned=%s, goal=%s/%s, achievements=%s",
            user_id,
            xp,
            level.get("level"),
            translations,
            favorites,
            learned,
            progress,
            target,
            len(achievements),
        )

        return ProfileData(
            language=language,

            xp=xp,

            level=level,

            translations=translations,

            favorites=favorites,

            learned_words=learned,

            goal_progress=progress,

            goal_target=target,

            achievements=achievements,
        )

    @staticmethod
    def build_progress_bar(
        progress: int,
        target: int
    ):
        """
        Строит progress bar из 10 символов.
        """

        if target <= 0:
            target = 10

        filled = int(
            progress / target * 10
        )

        filled = min(
            filled,
            10
        )

        return (
            "█" * filled
            +
            "░" * (10 - filled)
        )

    @staticmethod
    def build_profile_text(
        profile: ProfileData
    ):
        """
        Формирует текст профиля для Telegram.
        """

        bar = ProfileService.build_progress_bar(
            profile.goal_progress,
            profile.goal_target,
        )

        return (
            "👤 Профиль\n\n"

            f"🌐 Язык: "
            f"{profile.language or 'не выбран'}\n\n"

            f"🏆 Уровень: "
            f"{profile.level['level']}\n"

            f"⭐ XP: "
            f"{profile.xp}\n"

            f"📈 До следующего уровня: "
            f"{profile.level['need_xp'] - profile.level['current_xp']} XP\n\n"

            f"📚 Переводов: "
            f"{profile.translations}\n"

            f"⭐ Избранных: "
            f"{profile.favorites}\n"

            f"🧠 Изучено слов: "
            f"{profile.learned_words}\n\n"

            f"🎯 Цель дня:\n"

            f"{bar} "
            f"{profile.goal_progress}/{profile.goal_target}\n\n"

            "🏅 Достижения:\n"

            + "\n".join(
                profile.achievements[:5]
            )
        )

    async def get_study_progress_text(
        self,
        user_id: int
    ):
        """
        Возвращает текст прогресса обучения.
        """
        logger.info(
            "получение прогресса обучения: user_id=%s",
            user_id,
        )

        try:
            progress = await self.repository.get_study_progress(
                user_id
            )
        except Exception:
            logger.exception(
                "ошибка при получении прогресса обучения: user_id=%s",
                user_id
            )
            raise

        logger.info(
            "прогресс обучение получен:"
            "user_id=%s, total=%s, learned=%s, difficult=%s",
            user_id,
            progress.get("total_words", 0),
            progress.get("learned_words", 0),
            progress.get("difficult_words", 0),
         )
        return (
            "📊 Прогресс обучения\n\n"

            f"📝 Всего слов: "
            f"{progress.get('total_words', 0)}\n"

            f"✅ Выучено: "
            f"{progress.get('learned_words', 0)}\n"

            f"❌ Сложные слова: "
            f"{progress.get('difficult_words', 0)}"
        )

    async def get_achievements_text(
        self,
        user_id: int
    ):
        """
        Возвращает текст достижений пользователя.
        """
        logger.info(
            "получение достижений: user_id=%s",
            user_id,
        )

        try:
            stats = await self.repository.get_statistics(
                user_id
            )

            xp = await self.repository.get_xp(
                user_id
            )

            learned = await self.repository.get_learned_words(
                user_id
            )

        except Exception:
            logger.exception(
                "ошибка при получении данных достижений: user_id=%s",
                user_id,
            )
            raise    

        # ==========================
        # Нормализация типов
        # ==========================

        try:
            xp = int(xp)
        except (TypeError, ValueError):
            logger.warning(
                "Некорректное значение XP для достижений,"
                "установлено 0: user_id=%s, value=%r",
                user_id,
                xp,
            )
            xp=0

        try:
            learned = int(learned)
        except (TypeError, ValueError):
            logger.warning(
                "некорректное количество изученных слов"
                "для достижений, установлено 0: user_id=%s, value=%s",
                user_id,
                learned
            )
            learned = 0

        translations = int(
            stats.get("translations", 0)
        )

        achievements = get_achievements(
            translations,
            xp,
            learned,
        )

        logger.info(
            "достижения рассчитаны: user_id=%s, count=%s",
            user_id,
            len(achievements),
        )

        return (
            "🏅 Достижения\n\n"

            + "\n".join(
                achievements
            )
        )

