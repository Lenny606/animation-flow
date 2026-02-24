import asyncio
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path to allow importing from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from app.models.song import Song

async def seed_songs():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    collection = db["songs"]

    data = {
      "playlist_name": "Klasické české lidové písničky",
      "category": "Lidová tvorba",
      "songs": [
        {
          "title": "Komáři se ženili",
          "text": "1. Komáři se ženili, bumbum, pili víno, komáři se ženili, pili víno. Nasedali na komáry, pili víno, nasedali na komáry, pili víno.\n2. Přiletěl tam slavíček, bumbum, rozbil jim tam, přiletěl tam slavíček, rozbil jim tam. Rozbil jim tam rendlíček, pili víno, rozbil jim tam rendlíček, pili víno.\n3. Komár leží v komoře, bumbum, muška pláče, komár leží v komoře, muška pláče. Muška pláče na dvoře, pili víno, muška pláče na dvoře, pili víno.\n4. Neplač, muško, co pláčeš, bumbum, však ti komár, neplač, muško, co pláčeš, však ti komár. Však ti komár vstane zas, pili víno, však ti komár vstane zas, pili víno.\n5. Nestaň, muško, nestaň už, bumbum, už je komár, nestaň, muško, nestaň už, už je komár. Už je komár nebožtík, pili víno, už je komár nebožtík, pili víno."
        },
        {
          "title": "Pec nám spadla",
          "text": "Pec nám spadla, pec nám spadla, kdopak nám ji postaví? Starý pecař není doma a mladý to neumí. Zavoláme na dědečka, ten má velké kladivo, dá do toho čtyři rány a už je to hotovo."
        },
        {
          "title": "Prší, prší, jen se leje",
          "text": "Prší, prší, jen se leje, kam koníčky pojedeme? Pojedeme na luka, až kukačka zakuká. Kukačka už zakukala, má panenka zaplakala. Ty kukačko, nekukej, má panenko, neplakej."
        },
        {
          "title": "Skákal pes přes oves",
          "text": "Skákal pes přes oves, přes zelenou louku, šel za ním myslivec, péro na klobouku. Pejsku náš, co děláš, žes tak vesel stále? Řek bych vám, nevím sám, hop a jel jsem dále."
        },
        {
          "title": "Šla Nanynka do zelí",
          "text": "Šla Nanynka do zelí, do zelí, do zelí, natrhala lupení, lupeníčko. Přišel na ni Pepíček, rozšlapal jí košíček. Ty, ty, ty, ty, ty, ty, ty to budeš platiti!"
        },
        {
          "title": "Kalamajka mik mik mik",
          "text": "Kalamajka mik mik mik, oženil se kominík. Vzal si ženu Elišku v roztrhaném kožíšku. Kalamajka pěkná věc, když je klobása i pec. Když je klobása uzená, to je holka rozmařená."
        }
      ]
    }

    print(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    print(f"Using database: {settings.DATABASE_NAME}")

    inserted_count = 0
    for song_data in data["songs"]:
        song = Song(
            title=song_data["title"],
            text=song_data["text"],
            playlist_name=data["playlist_name"],
            category=data["category"]
        )
        
        # Check if song already exists to avoid duplicates
        existing = await collection.find_one({"title": song.title, "playlist_name": song.playlist_name})
        if not existing:
            await collection.insert_one(song.model_dump(by_alias=True, exclude_none=True))
            print(f"Inserted: {song.title}")
            inserted_count += 1
        else:
            print(f"Skipped (already exists): {song.title}")

    print(f"Seeding completed. Inserted {inserted_count} songs.")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_songs())
