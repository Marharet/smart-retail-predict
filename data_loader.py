import pandas as pd
from db.db_config import engine, SessionLocal, Base
from db.models.product import Product
from db.models.sales_record import SalesRecord

# cтворення таблиць 
Base.metadata.create_all(bind=engine)

def load_data(file_path):
    db = SessionLocal()
    try:
        df = pd.read_csv(file_path)
        
        df = df.dropna()
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        
        unique_products = df[['Product', 'Price Each']].drop_duplicates('Product')
        
        product_map = {} # для швидкого пошуку ID за назвою
        
        for _, row in unique_products.iterrows():
            product = db.query(Product).filter(Product.name == row['Product']).first()
            if not product:
                product = Product(name=row['Product'], price=float(row['Price Each']))
                db.add(product)
                db.flush() 
            product_map[product.name] = product.id
        db.commit()
        

        batch_size = 500
        records_to_add = []
        
        for index, row in df.iterrows():
            new_sale = SalesRecord(
                order_id=str(row['Order ID']),
                product_id=product_map[row['Product']], # Foreign key
                quantity_ordered=int(row['Quantity Ordered']),
                order_date=row['Order Date']
            )
            records_to_add.append(new_sale)
            
            if len(records_to_add) >= batch_size:
                db.bulk_save_objects(records_to_add)
                db.commit()
                records_to_add = []
        
        if records_to_add:
            db.bulk_save_objects(records_to_add)
            db.commit()
                    
    except Exception as e:
        print(f"Loading error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_data('data/Electronic_Sales.csv')