import os
import pandas as pd
import numpy as np

# =====================================================================
# GENERACIÓN DE DATOS FICTICIOS (data_1.pqt y data_2.pqt)
# =====================================================================
print("Generando datos ficticios de prueba local...")

# Creamos 5 usuarios de prueba
usuarios_prueba = [f'user_{i}' for i in range(1, 6)]

# Generamos data_1 (datos de estudiantes)
df_estudiantes = pd.DataFrame({
    'user_uuid': usuarios_prueba,
    'verified': [True, False, True, True, False],
    'grade': [0.85, 0.90, np.nan, 0.70, 0.60]  # El usuario 3 simula una nota faltante (NaN)
})
df_estudiantes.to_parquet('data_1.pqt')

# Generamos data_2 (actividades diarias)
df_eventos = pd.DataFrame({
    'user_uuid': np.random.choice(usuarios_prueba, size=25),
    'date': pd.date_range(start='2026-10-01', periods=25, freq='D'),
    'nevents': np.random.randint(1, 10, size=25),
    'nproblem_check': np.random.randint(0, 5, size=25)
})
df_eventos.to_parquet('data_2.pqt')


# =====================================================================
# TU CÓDIGO PROCESANDO LOS ARCHIVOS LOCALES
# =====================================================================

### TEST FUNCTION: test_load_data
# Modificado para leer los archivos locales que acabamos de crear
students_df = pd.read_parquet('data_1.pqt')
events_df = pd.read_parquet('data_2.pqt')


### TEST FUNCTION: test_filter_population
# Mantenemos tu lógica intacta usando verified_cols[0] de forma segura
verified_cols = [col for col in students_df.columns if 'verified' in col.lower()]

if len(verified_cols) > 0:
    # Agregamos .copy() para evitar advertencias de copia en Pandas local
    modeling_pop_df = students_df[(students_df[verified_cols[0]] == True) & (students_df['grade'].notna())].copy()
else:
    modeling_pop_df = students_df[students_df['grade'].notna()].copy()


### TEST FUNCTION: test_first_event
events_df['date'] = pd.to_datetime(events_df['date'])
first_event_df = events_df.groupby('user_uuid')['date'].min().reset_index()
first_event_df = first_event_df.rename(columns={'date': 'first_event_date'})


### TEST FUNCTION: test_merge_first_event
events_df = events_df.merge(first_event_df, on='user_uuid', how='left')


### TEST FUNCTION: test_cutoff_date
events_df['cutoff_date'] = events_df['first_event_date'] + pd.Timedelta(days=14)


### TEST FUNCTION: test_early_events
early_events_df = events_df[events_df['date'] <= events_df['cutoff_date']].copy()


### TEST FUNCTION: test_aggregate_activity
activity_cols = [col for col in early_events_df.columns if col not in ['user_uuid', 'date', 'first_event_date', 'cutoff_date']]
early_activity_agg = early_events_df.groupby('user_uuid')[activity_cols].sum().reset_index()


### TEST FUNCTION: test_rename_columns
rename_dict = {col: f'early_{col}' for col in early_activity_agg.columns if col != 'user_uuid'}
early_activity_agg = early_activity_agg.rename(columns=rename_dict)


### TEST FUNCTION: test_merge_data
final_df = modeling_pop_df.merge(early_activity_agg, on='user_uuid', how='left')


### TEST FUNCTION: test_fill_na
early_cols = [col for col in final_df.columns if col.startswith('early_')]
final_df[early_cols] = final_df[early_cols].fillna(0)


### TEST FUNCTION: test_save_data
import os

os.makedirs('data', exist_ok=True)
final_df.to_parquet('data/final_df.pqt')

print("¡Proceso completado! Archivo guardado localmente en 'data/final_df.pqt'")
print("\nResultado en final_df:")
print(final_df)