import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from lecture_06.part_1.data_generator import create_dataset_local
create_dataset_local() 

# Set a default style for our plots for consistency.
sns.set_style("whitegrid")


### TEST FUNCTION: test_load_data
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
students_df = pd.read_parquet('person_course.pqt')

students_df.head()


### TEST FUNCTION: test_missing_values
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
missing_values = students_df.isnull().sum()
missing_values


### TEST FUNCTION: test_missing_percentage
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
missing_percentage = (students_df.isnull().sum() / len(students_df)) * 100
missing_percentage


### TEST FUNCTION: test_missing_df
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
missing_info = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage': missing_percentage
})

missing_info = missing_info.sort_values(by='Missing Values', ascending=False)
missing_info


### TEST FUNCTION: test_grade_histogram
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
grades_clean = students_df['grade'].dropna()

plt.figure(figsize=(8, 5))
sns.histplot(grades_clean, bins=20, kde=True)
plt.title('final grade distribution (Grade)')
plt.xlabel('Grades')
plt.ylabel('Frequency')
plt.show()


### TEST FUNCTION: test_certification_rate
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
cert_proportion = students_df['certified'].value_counts(normalize=True)
cert_proportion


### TEST FUNCTION: test_enrollment_plot
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
plt.figure(figsize=(8, 5))
sns.countplot(data=students_df, x='mode', hue='certified')
plt.title('Relation between Enrollment Mode and Certification Mode')
plt.xlabel('Enrollment Mode')
plt.ylabel('Students quantity')
plt.legend(title='Certificate', labels=['Falso (False)', 'Verdadero (True)'])
plt.show()


### TEST FUNCTION: test_enrollment_crosstab
# DO NOT REMOVE THE LINE ABOVE
# TODO: Write your solution here. Your code is required before running this notebook.
enrollment_crosstab = pd.crosstab(students_df['mode'], students_df['certified'])

print("Enrollment Crosstab:")
print(enrollment_crosstab)
