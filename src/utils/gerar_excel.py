import pandas as pd
import io

def to_excel(df, totais=None):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Filtrados")
        writer.sheets["Filtrados"] = worksheet

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#D9D9D9",
            "border": 1,
            "align": "center"
        })

        currency_format = workbook.add_format({
            "num_format": '#,##0.00',
            "border": 1
        })

        cell_format = workbook.add_format({"border": 1})

        cols_to_write = [c for c in df.columns if c != "auto_unique_id"]
        cols_to_write = [c for c in df.columns if c != "Selecionar ✅"]
        cols_to_write = [c for c in df.columns if c != "Selecionar"]
        for col_idx, col_name in enumerate(cols_to_write):
            worksheet.write(0, col_idx, col_name, header_format)

        for row_idx in range(len(df)):
            for col_idx, col_name in enumerate(cols_to_write):
                val = df.iloc[row_idx][col_name]
                if isinstance(val, (int, float)):
                    fmt = currency_format
                elif pd.api.types.is_datetime64_any_dtype(df[col_name]):
                    fmt = workbook.add_format({"num_format": "dd/mm/yyyy hh:mm", "border": 1})
                else:
                    fmt = cell_format
                worksheet.write(row_idx + 1, col_idx, val, fmt)

        if totais is not None:
            total_row_index = len(df) + 1
            worksheet.write(total_row_index, 0, "TOTAL", header_format)

            for col_idx, col_name in enumerate(cols_to_write[1:], start=1):
                if col_name in totais.index:
                    val = totais[col_name]
                    worksheet.write(total_row_index, col_idx, val, currency_format)
                else:
                    worksheet.write(total_row_index, col_idx, "", cell_format)

        for col_idx, col_name in enumerate(cols_to_write):
            max_len = max(
                df[col_name].astype(str).map(len).max(),
                len(col_name)
            ) + 2
            worksheet.set_column(col_idx, col_idx, max_len)

    output.seek(0)
    return output
