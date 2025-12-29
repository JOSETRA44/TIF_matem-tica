# En df_data (COU): mapear códigos a 10 sectores
sector_codes = {
    0: ['001001','001002',...,'009999'],  # Agri/Pesca (65 códigos aprox)
    1: ['010001','010002',...,'019999'],  # Minería (10 códigos)
    # ... hasta 9
}
U_agg = np.zeros((10,10))
for i, prods in sector_codes.items():
    for j, acts in sector_codes.items():
        mask_prod = df_data.iloc[:,0].astype(str).str.startswith(prods)
        mask_act = [col.startswith(acts) for col in df_data.columns[11:112]]
        U_agg[i,j] = df_data.loc[mask_prod, mask_act].sum().sum()
