import pandas as pd
import numpy as np
import os

np.random.seed(42)
n_students = 5000

print(f"Generating learning analytics dataset for {n_students} students...")

data = {
    'grade': np.random.beta(a=2, b=5, size=n_students), 
    'certified': np.random.choice([0, 1], size=n_students, p=[0.75, 0.25]), 
    'early_nevents': np.random.negative_binomial(n=10, p=0.05, size=n_students),
    'assignment_views': np.random.poisson(lam=15, size=n_students),
    'forum_posts': np.random.negative_binomial(n=1, p=0.3, size=n_students),
    'video_chapters_watched': np.random.randint(0, 40, size=n_students),
    'browser_language': np.random.choice(['en', 'es', 'fr', 'pt'], size=n_students, p=[0.5, 0.3, 0.1, 0.1]),
    'user_country': np.random.choice(['USA', 'UK', 'Spain', 'Mexico', 'Other'], size=n_students)
}

final_df = pd.DataFrame(data)

# Detectar la ruta exacta de la carpeta actual donde reside este script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'student_data.pqt')

final_df.to_parquet(output_path, index=False)
print(f"Dataset successfully created and saved to absolute path: '{output_path}'")