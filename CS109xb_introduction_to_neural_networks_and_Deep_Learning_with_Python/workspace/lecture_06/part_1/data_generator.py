import pandas as pd
import numpy as np

def create_dataset_local():
    np.random.seed(42)
    n_students = 200

    data = {
        'grade': [np.random.randint(50, 100) if np.random.rand() > 0.15 else np.nan for _ in range(n_students)],
        'certified': np.random.choice([True, False], size=n_students, p=[0.25, 0.75]),
        'mode': np.random.choice(['verified', 'audit'], size=n_students, p=[0.35, 0.65]),
        'gender': np.random.choice(['M', 'F', 'Other'], size=n_students),
        'LoE': np.random.choice(['Bachelor', 'Master', 'High School'], size=n_students)
    }

    simulated_df = pd.DataFrame(data)
    
    # Guarda el archivo directamente usando la ruta relativa simple
    simulated_df.to_parquet('person_course.pqt')
    print("✨ File 'person_course.pqt' generated successfully thanks to data_generator.")

if __name__ == '__main__':
    create_dataset_local()
