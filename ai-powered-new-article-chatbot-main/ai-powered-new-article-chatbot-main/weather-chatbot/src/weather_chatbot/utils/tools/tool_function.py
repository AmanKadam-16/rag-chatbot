from src.weather_chatbot.database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text


class ModelFunctions:

    @staticmethod
    def get_continent_weather_context(param_dict):
        db: Session = next(get_db())
        try:
            sql_query_str = param_dict.get("sql_query")
            print(f"\nSQL Query >> {sql_query_str}\n")
            if not sql_query_str:
                return {"error": "Missing 'sql_query' parameter."}
            sql_query = text(sql_query_str)
            result = db.execute(sql_query)
            db.commit()
            if result.returns_rows:
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows]
        except Exception as e:
            return {"error": str(e)}
