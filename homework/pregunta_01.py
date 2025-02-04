def pregunta_01():
    import pandas as pd
    from unidecode import unidecode

    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    # Leer el archivo
    df = pd.read_csv("./files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
    df.dropna(inplace=True)

    # Columnas de texto
    txt_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for column in txt_columns:
        df[column] = df[column].apply(
            lambda x: unidecode(str(x))
            .lower()
            .strip()
            .strip("-")
            .strip("_")
            .replace(" ", "_")
            .replace("-", "_")
        )

    # Convertir fechas al formato YYYY-MM-DD
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], errors="coerce", dayfirst=True
    )

    # Normalizar idea de negocio
    df["idea_negocio"] = df["idea_negocio"].apply(
        lambda x: (
            "_".join(x.split("_")[:-1]).strip("_")
            if x.split("_")[-1] in ("de", "en", "el", "y")
            else x
        )
    )

    # Convertir monto_del_credito a número
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .replace(r"[\$,]", "", regex=True)
        .astype(float)
        .astype(int)
    )

    # Corregir estrato y comuna
    df["estrato"] = (
        df["estrato"].astype(str).str.replace("[^0-9]", "", regex=True).astype(int)
    )
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(float).astype(int)

    # Corregir barrios
    # Corregir numeraciones
    df["barrio"] = df["barrio"].apply(
        lambda x: str(x).replace("no.", "no_").replace("no ", "no_").replace("__", "_")
    )

    # Corregir caracteres faltantes
    df["barrio"] = df["barrio"].apply(
        lambda x: str(x).replace("bel?n", "belen").replace(".", "").replace("?", "ñ")
    )

    # Eliminar duplicados
    df.drop_duplicates(inplace=True)

    print(df["barrio"].unique())
    print(len(df["barrio"].unique()))
    print(df.head)

    # Guardar el archivo limpio
    df.to_csv("./files/output/solicitudes_de_credito.csv", sep=";", index=False)


pregunta_01()
