import asyncio
from decimal import Decimal

from sqlalchemy import func, select

from app.database import AsyncSession, SessionLocal, init_db
from app.models.category import Category
from app.models.product import Product


async def create_categories(db: AsyncSession) -> dict[str, Category]:
    """Создает категории товаров асинхронно."""
    categories_data = [
        {"name": "Voice Tags", "slug": "voice-tags"},
        {"name": "Mixing", "slug": "mixing"},
    ]

    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        categories[cat_data["slug"]] = category

    await db.commit()  # <-- Асинхронный commit

    # Обновляем объекты после commit для получения ID
    for category in categories.values():
        await db.refresh(category)  # <-- Асинхронный refresh

    return categories


async def create_products(db: AsyncSession, categories: dict[str, Category]) -> None:
    """Создает товары асинхронно."""
    products_data = [
        {
            "name": "Войс тег BASED",
            "description": "Высокое качество записи. Вы получаете 2 сведенных войс тега с одной фразой.",
            # Важно: используем Decimal для цен, как настроено в модели
            "price": Decimal("12.99"),
            "category_id": categories["voice-tags"].id,
            "image_url": "https://i.imgur.com/i8qx9CR.jpeg",
        },
        {
            "name": "Войс тег BULK (1+1)",
            "description": "Высокое качество записи. Вы получаете 4 сведенных войс тега с двумя разными фразами.",
            "price": Decimal("23.99"),
            "category_id": categories["voice-tags"].id,
            "image_url": "https://i.imgur.com/trtdq16.jpeg",
        },
        {
            "name": "Сведение (2 mixes)",
            "description": "Сведение записи (высокое качество). Вы получаете 2 сведенных войс тега из одного исходника.",
            "price": Decimal("5.99"),
            "category_id": categories["mixing"].id,
            "image_url": "https://i.imgur.com/NNLvlo6.jpeg",
        },
    ]

    for product_data in products_data:
        product = Product(**product_data)
        db.add(product)

    await db.commit()  # <-- Асинхронный commit
    print(f"✅ Created {len(products_data)} products")


async def seed_database() -> None:
    """Главная асинхронная функция для заполнения базы данных."""
    print("🚀 Starting database seeding...")

    # Инициализируем БД (создаем таблицы)
    await init_db()
    print("✅ Database tables created")

    # Безопасное открытие асинхронной сессии через async with
    async with SessionLocal() as db:
        try:
            # Исправлено: Асинхронный подсчет количества категорий
            statement = select(func.count(Category.id))
            result = await db.execute(statement)
            existing_categories = result.scalar_one()

            if existing_categories > 0:
                print("⚠️  Database already contains data. Skipping seed.")
                return

            # Создаем категории
            print("📁 Creating categories...")
            categories = await create_categories(db)
            print(f"✅ Created {len(categories)} categories")

            # Создаем товары
            print("📦 Creating products...")
            await create_products(db, categories)

            print("🎉 Database seeding completed successfully!")

        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            await db.rollback()  # <-- Асинхронный rollback


if __name__ == "__main__":
    asyncio.run(seed_database())
