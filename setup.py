from setuptools import setup, find_packages

setup(
    name="PKTFUNC",
    version="0.2",  
    packages=find_packages(),
    package_data={
        'PKTFUNC': ['Datos/TABLAS.xlsx'],
    },
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'openpyxl',
    ],
    author="Mallo Jorge, Bernal Alejandro",
    author_email="",
    description="Un paquete para cálculos actuariales",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jorge99MM/PKTFUNCpy",
)