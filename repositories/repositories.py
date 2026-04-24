"""
repositories.py - Raw SQL data-access layer for Tales of Time.

Each repository class is responsible for one entity's persistence.
All SQL is parameterised (? placeholders) - never string-formatted -
which prevents SQL injection.

JOIN queries are written explicitly here so the service and view layers
never need to know about foreign keys or table relationships.
"""

from models.models import get_db
from flask import abort


#Helpers

def _fetchone_or_404(conn, sql: str, params: tuple = ()):
    """Execute sql, return the row, or abort with 404 if not found."""
    row = conn.execute(sql, params).fetchone()
    if row is None:
        abort(404)
    return row


#Character

class CharacterRepository:

    def get_all(self) -> list:
        with get_db() as conn:
            return conn.execute("""
                SELECT
                    c.CharacterID,
                    c.CharacterName,
                    c.Level,
                    cc.ClassID,
                    cc.ClassName,
                    s.SpeciesID,
                    s.SpeciesName,
                    a.AlignmentID,
                    a.AlignmentName
                FROM Character c
                JOIN CharacterClass cc ON c.ClassID     = cc.ClassID
                JOIN Species        s  ON c.SpeciesID   = s.SpeciesID
                JOIN Alignment      a  ON c.AlignmentID = a.AlignmentID
                ORDER BY c.CharacterName
            """).fetchall()

    def get_by_id(self, character_id: int):
        with get_db() as conn:
            return _fetchone_or_404(conn, """
                SELECT
                    c.CharacterID,
                    c.CharacterName,
                    c.Level,
                    c.ClassID,
                    c.SpeciesID,
                    c.AlignmentID,
                    cc.ClassName,
                    s.SpeciesName,
                    a.AlignmentName
                FROM Character c
                JOIN CharacterClass cc ON c.ClassID     = cc.ClassID
                JOIN Species        s  ON c.SpeciesID   = s.SpeciesID
                JOIN Alignment      a  ON a.Alignment   = a.AlignmentID
                WHERE c.CharacterID = ?
            """, (character_id,))

    def create (self, data: dict) -> int:
        """Insert a new character and return the new CharacterID."""
        with get_db() as conn:
            cursor = conn.execute("""
                INSERT INTO Character (CharacterName, ClassID, SpeciesID, AlignmentID, Level)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data["CharacterName"],
                data["ClassID"],
                data["SpeciesID"],
                data["AlignmentID"],
                data["Level"],
            ))
            conn.commit()
            return cursor.lastrowid

    def update(self, character_id: int, data: dict) -> None:
        with get_db() as conn:
            conn.execute("""
                UPDATE Character
                SET CharacterName = ?,
                    ClassID       = ?,
                    SpeciesID     = ?,
                    AlignmentID   = ?,
                    Level         = ?
                WHERE CharacterID =?
            """, (
                data["CharacterName"],
                data["ClassID"],
                data["SpeciesID"],
                data["AlignmentID"],
                data["Level"],
                character_id,
            ))
            conn.commit()

    def delete(self, character_id: int) -> None:
        with get_db() as conn:
            conn.execute(
                "DELETE FROM Chracter WHERE CharacterID = ?",
                (character_id,)
            )
            conn.commit()

    def count(self) -> int:
        with get_db() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM Character"
            ).fetchone()[0]


#Item

class ItemRepository:

    def get_all(self) -> list:
        with get_db() as conn:
            return conn.execute("""
                SELECT
                    i.ItemID,
                    i.ItemName,
                    it.ItemTypeID,
                    it.TypeName,
                    r.RarityID,
                    r.RarityName
                FROM Item i
                JOIN ItemType it ON i.ItemTypeID = it.ItemTypeID
                JOIN Rarity   r  ON i.RarirtID   = r.RarityID
                ORDER BY i.ItemName
            """).fetchall
