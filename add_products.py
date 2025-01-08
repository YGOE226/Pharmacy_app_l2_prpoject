from app import app,db
from app.models import Product

def add_products():
    products = [
        {"name": "Paracetamol", "description": "Pain reliever", "quantity": 100, "price": 2.5},
        {"name": "Ibuprofen", "description": "Anti-inflammatory", "quantity": 150, "price": 3.0},
        {"name": "Amoxicillin", "description": "Antibiotic", "quantity": 200, "price": 5.0},
        {"name": "Aspirin", "description": "Pain reliever", "quantity": 120, "price": 1.5},
        {"name": "Cetirizine", "description": "Allergy medication", "quantity": 130, "price": 4.0},
        {"name": "Metformin", "description": "Diabetes medication", "quantity": 140, "price": 8.0},
        {"name": "Omeprazole", "description": "Acid reflux treatment", "quantity": 90, "price": 6.5},
        {"name": "Atorvastatin", "description": "Cholesterol medication", "quantity": 110, "price": 10.0},
        {"name": "Simvastatin", "description": "Cholesterol medication", "quantity": 115, "price": 9.0},
        {"name": "Lisinopril", "description": "High blood pressure medication", "quantity": 130, "price": 7.0},
        {"name": "Losartan", "description": "High blood pressure medication", "quantity": 150, "price": 6.0},
        {"name": "Amlodipine", "description": "High blood pressure medication", "quantity": 160, "price": 8.5},
        {"name": "Furosemide", "description": "Diuretic", "quantity": 170, "price": 3.5},
        {"name": "Prednisone", "description": "Steroid", "quantity": 180, "price": 5.5},
        {"name": "Hydrochlorothiazide", "description": "Diuretic", "quantity": 190, "price": 4.5},
        {"name": "Levothyroxine", "description": "Thyroid hormone", "quantity": 140, "price": 6.5},
        {"name": "Albuterol", "description": "Asthma inhaler", "quantity": 100, "price": 15.0},
        {"name": "Gabapentin", "description": "Nerve pain medication", "quantity": 120, "price": 9.5},
        {"name": "Citalopram", "description": "Antidepressant", "quantity": 130, "price": 7.5},
        {"name": "Sertraline", "description": "Antidepressant", "quantity": 140, "price": 8.0},
        {"name": "Escitalopram", "description": "Antidepressant", "quantity": 150, "price": 7.0},
        {"name": "Trazodone", "description": "Antidepressant", "quantity": 160, "price": 6.0},
        {"name": "Fluoxetine", "description": "Antidepressant", "quantity": 170, "price": 9.0},
        {"name": "Venlafaxine", "description": "Antidepressant", "quantity": 180, "price": 8.5},
        {"name": "Duloxetine", "description": "Antidepressant", "quantity": 190, "price": 9.5},
        {"name": "Bupropion", "description": "Antidepressant", "quantity": 200, "price": 10.5},
        {"name": "Mirtazapine", "description": "Antidepressant", "quantity": 140, "price": 7.5},
        {"name": "Atenolol", "description": "Beta-blocker", "quantity": 150, "price": 4.0},
        {"name": "Metoprolol", "description": "Beta-blocker", "quantity": 160, "price": 5.0},
        {"name": "Propranolol", "description": "Beta-blocker", "quantity": 170, "price": 6.0},
        {"name": "Carvedilol", "description": "Beta-blocker", "quantity": 180, "price": 7.0},
        {"name": "Bisoprolol", "description": "Beta-blocker", "quantity": 190, "price": 6.5},
        {"name": "Clopidogrel", "description": "Blood thinner", "quantity": 200, "price": 8.5},
        {"name": "Warfarin", "description": "Blood thinner", "quantity": 140, "price": 9.5},
        {"name": "Apixaban", "description": "Blood thinner", "quantity": 150, "price": 12.0},
        {"name": "Rivaroxaban", "description": "Blood thinner", "quantity": 160, "price": 11.0},
        {"name": "Digoxin", "description": "Heart medication", "quantity": 170, "price": 10.0},
        {"name": "Amiodarone", "description": "Heart rhythm medication", "quantity": 180, "price": 14.0},
        {"name": "Lidocaine", "description": "Local anesthetic", "quantity": 190, "price": 3.0},
        {"name": "Fentanyl", "description": "Pain relief", "quantity": 200, "price": 20.0},
        {"name": "Morphine", "description": "Pain relief", "quantity": 100, "price": 18.0},
        {"name": "Oxycodone", "description": "Pain relief", "quantity": 120, "price": 15.0},
        {"name": "Hydrocodone", "description": "Pain relief", "quantity": 130, "price": 14.0},
        {"name": "Codeine", "description": "Pain relief", "quantity": 140, "price": 13.0},
        {"name": "Tramadol", "description": "Pain relief", "quantity": 150, "price": 12.0},
        {"name": "Acyclovir", "description": "Antiviral", "quantity": 160, "price": 10.0},
        {"name": "Valacyclovir", "description": "Antiviral", "quantity": 170, "price": 11.0},
        {"name": "Oseltamivir", "description": "Antiviral", "quantity": 180, "price": 9.0},
        {"name": "Zidovudine", "description": "HIV medication", "quantity": 190, "price": 15.0},
        {"name": "Efavirenz", "description": "HIV medication", "quantity": 200, "price": 17.0},
        {"name": "Ritonavir", "description": "HIV medication", "quantity": 140, "price": 16.0},
        {"name": "Lopinavir", "description": "HIV medication", "quantity": 150, "price": 18.0},
        {"name": "Insulin", "description": "Diabetes medication", "quantity": 160, "price": 30.0},
        {"name": "Glipizide", "description": "Diabetes medication", "quantity": 170, "price": 12.0},
        {"name": "Glyburide", "description": "Diabetes medication", "quantity": 180, "price": 13.0},
        {"name": "Pioglitazone", "description": "Diabetes medication", "quantity": 190, "price": 14.0},
        {"name": "Sitagliptin", "description": "Diabetes medication", "quantity": 200, "price": 15.0},
        {"name": "Canagliflozin", "description": "Diabetes medication", "quantity": 140, "price": 25.0},
        {"name": "Empagliflozin", "description": "Diabetes medication", "quantity": 150, "price": 24.0},
        {"name": "Dapagliflozin", "description": "Diabetes medication", "quantity": 160, "price": 23.0},
        {"name": "Spironolactone", "description": "Diuretic", "quantity": 170, "price": 7.0},
        {"name": "Eplerenone", "description": "Diuretic", "quantity": 180, "price": 8.0},
        {"name": "Torsemide", "description": "Diuretic", "quantity": 190, "price": 6.0},
    ]

    with app.app_context():  # Active le contexte d'application Flask
        for product in products:
            new_product = Product(
                name=product["name"],
                description=product["description"],
                quantity=product["quantity"],
                price=product["price"]
            )
            db.session.add(new_product)
        db.session.commit()

if __name__ == '__main__':
    add_products()
