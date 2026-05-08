import asyncio
import os
import sys
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Add the backend directory to sys.path to allow importing from app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

async def seed_songs():
    # Load .env from backend directory
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)
    
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("DATABASE_NAME", "animation_flow_db")
    
    print(f"Connecting to: {mongodb_url}")
    print(f"Target Database: {db_name}")
    
    client = AsyncIOMotorClient(mongodb_url)
    db = client[db_name]
    collection = db["songs"]
    
    songs = [
        {
            "title": "Prší, prší, jen se leje",
            "text": "Prší, prší, jen se leje, kam koníčky pojedeme? Pojedeme na luka, až kukačka zakuká. Kukačka už zakukala, má panenka zaplakala. Ty kukačko, nekukej, má panenko, neplakej.",
            "playlist_name": "Klasické české lidové písničky",
            "category": "Lidová tvorba",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Skákal pes přes oves",
            "text": "Skákal pes přes oves, přes zelenou louku, šel za ním myslivec, péro na klobouku. Pejsku náš, co děláš, žes tak vesel stále? Řek bych vám, nevím sám, hop a jel jsem dále.",
            "playlist_name": "Klasické české lidové písničky",
            "category": "Lidová tvorba",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Šla Nanynka do zelí",
            "text": "Šla Nanynka do zelí, do zelí, do zelí, natrhala lupení, lupeníčko. Přišel na ni Pepíček, rozšlapal jí košíček. Ty, ty, ty, ty, ty, ty, ty to budeš platiti!",
            "playlist_name": "Klasické české lidové písničky",
            "category": "Lidová tvorba",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Kalamajka mik mik mik",
            "text": "Kalamajka mik mik mik, oženil se kominík. Vzal si ženu Elišku v roztrhaném kožíšku. Kalamajka pěkná věc, když je klobása i pec. Když je klobása uzená, to je holka rozmařená.",
            "playlist_name": "Klasické české lidové písničky",
            "category": "Lidová tvorba",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Pec nám spadla",
            "text": "Pec nám spadla, pec nám spadla, kdopak nám ji postaví? Starý pecař není doma a mladý to neumí. Zavoláme na dědečka, ten má velký kladivo, dá do toho čtyři rány a už je to hotovo.",
            "playlist_name": "Klasické české lidové písničky",
            "category": "Lidová tvorba",
            "created_at": datetime.utcnow()
        }
    ]
    
    for song in songs:
        # Check if song already exists to avoid duplicates
        existing = await collection.find_one({"title": song["title"]})
        if not existing:
            await collection.insert_one(song)
            print(f"Added: {song['title']}")
        else:
            print(f"Skipped (already exists): {song['title']}")
            
    print("Seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_songs())
