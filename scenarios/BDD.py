# Pour chaque ligne dans final_df
for index, row in final_df.iterrows():
    # Pour chaque table
    for table in tables:
        table_name = table["name"]
        columns = table["columns"]
        
        # Connexion à la base de données
        with engine.connect() as conn:
            try:
                # Supprimer les anciennes lignes de la table avant d'insérer les nouvelles
                delete_sql = text(f"DELETE FROM {table_name};")
                conn.execute(delete_sql)  # Exécute la suppression
                print(f"Deleted all rows from {table_name}")
                
                # Sélectionner les colonnes à insérer en fonction de `columns`
                row_to_insert = row[[key for key in columns.keys() if key in final_df.columns]].dropna()

                # Ajouter les colonnes spécifiées dans `add` (si elles sont définies)
                for add_column in table.get("add", []):
                    column_name = add_column["name"]
                    column_value = add_column["value"]

                    # Parcourir toutes les tables pour trouver la table qui correspond à `column_value`
                    for ref_table in tables:
                        if column_value == ref_table["name"]:
                            # Si l'ID de la table référencée est défini, on remplace la valeur de la colonne par l'ID
                            if ref_table["id"] is not None:
                                row_to_insert[column_name] = ref_table["id"]
                                print(f"Assigning ID from table '{ref_table['name']}' ({ref_table['id']}) to column '{column_name}' for row {row['annee']}")

                # Si la ligne à insérer est vide après le filtrage, passer à la ligne suivante
                if row_to_insert.empty:
                    print(f"Skipping year {row['annee']} as no valid data found for table {table_name}.")
                    continue

                # Construire la chaîne des colonnes à insérer
                columns_str = ", ".join(row_to_insert.index)
                # Créer les placeholders pour les valeurs
                placeholders = ", ".join([f":{col}" for col in row_to_insert.index])
                print(row, "roww")
                # Créer la requête SQL pour l'insertion
                insert_sql = text(f"""
                    INSERT INTO {table_name} ({columns_str})
                    VALUES ({placeholders})
                    RETURNING id;
                """)
                print("sql", insert_sql)
                # Exécuter l'insertion
                result = conn.execute(insert_sql, row_to_insert.to_dict())
                # Récupérer l'ID auto-incrémenté retourné par la requête
                inserted_id = result.scalar()
                print(f"Inserted row for year {row['annee']} into table {table_name} with ID: {inserted_id}")
                table["id"] = inserted_id  # Mettre à jour l'ID de la table après insertion
                conn.commit()  # Valider la transaction
            except Exception as e:
                # En cas d'erreur, rollback de la transaction
                conn.rollback()
                print(f"Error inserting row for year {row['annee']} into table {table_name}: {e}")
