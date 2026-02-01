import pandas as pd
import joblib
from sqlalchemy import select
from db.db_config import SessionLocal
from db.models.product import Product
from db.models.sales_record import SalesRecord
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score 


def fetch_data_from_db():
    session = SessionLocal()
    query = select(
        SalesRecord.order_date,
        SalesRecord.quantity_ordered,
        Product.id.label('product_id'),
        Product.name
    ).join(Product)
    
    df = pd.read_sql(query, session.bind)
    session.close()
    return df


def prepare_features(df):
    df['hour'] = df['order_date'].dt.hour
    df['day_of_week'] = df['order_date'].dt.dayofweek
    df['month'] = df['order_date'].dt.month
    
    # X  - ознаки; y - кількість (що прогнозуємо)
    X = df[['product_id', 'hour', 'day_of_week', 'month']]
    y = df['quantity_ordered']
    
    return X, y


def train_model():
    df = fetch_data_from_db()
    X, y = prepare_features(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, 'sales_model.pkl')


    # оцінка точності
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean absolute error: {mae:.2f}') # показує, на скільки одиниць товару в середньому помиляється модель
    print(f'R2 score: {r2:.2f}') # чим ближче до 1.0, тим краща модель


if __name__ == "__main__":
    train_model()