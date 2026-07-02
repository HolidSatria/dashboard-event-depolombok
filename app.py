import streamlit as st
import pandas as pd

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Event Toko",
    page_icon="🏪",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    "Form Pendataan Event Juli 2026.csv",
    sep=";",
    header=None,
    encoding="cp1252"
)

df.columns = df.iloc[2]
df = df.iloc[4:].reset_index(drop=True)

# Bersihkan nama kolom
df.columns = df.columns.astype(str).str.strip()

# =========================
# NAMA KOLOM PIC EVENT
# =========================
PIC_COL = "PIC EVENT\n(Wajib Isi)"

# =========================
# FUNGSI TARGET
# =========================
def hitung_target(series):

    total = pd.to_numeric(
        series.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False),
        errors="coerce"
    ).sum()

    return total


def format_target(nilai):

    return f"{nilai:,.0f}".replace(",", ".")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🏪 Event Dashboard")

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "🔎 Cari KDTK",
        "👤 Cari AM",
        "🧑‍💼 Cari AS",
        "📅 Cari Tanggal"
    ]
)

st.sidebar.info(
    "Dashboard pencarian event toko berdasarkan KDTK, AM, AS, dan Tanggal."
)

# =========================
# HEADER
# =========================
st.title("🏪 Dashboard Event Toko")

st.caption(
    "Pencarian Event Berdasarkan KDTK, AM, AS, dan Tanggal"
)

# ==================================================
# MENU KDTK
# ==================================================
if menu == "🔎 Cari KDTK":

    st.subheader("🔎 Cari Berdasarkan KDTK")

    kode = st.text_input(
        "Masukkan KDTK",
        placeholder="Contoh: TICK"
    )

    if kode:

        hasil = df[
            df['KDTK\n(Wajib Isi)']
            .astype(str)
            .str.upper()
            == kode.upper()
        ]

        if hasil.empty:

            st.error("KDTK tidak ditemukan")

        else:

            toko = hasil.iloc[0]

            st.success("Data ditemukan")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "KDTK",
                    toko['KDTK\n(Wajib Isi)']
                )

            with col2:
                st.metric(
                    "AS",
                    toko['AS\n(Rumus)']
                )

            with col3:
                st.metric(
                    "AM",
                    toko['AM\n(Rumus)']
                )

            with col4:

                if 'Target' in hasil.columns:

                    target_toko = hitung_target(
                        hasil['Target']
                    )

                    st.metric(
                        "Target",
                        format_target(target_toko)
                    )

            st.info(
                f"🏪 {toko['NAMA TOKO\n(Rumus)']}"
            )

            st.subheader("📅 Jadwal Event")

            kolom = [
                'TGL EVENT\n(Wajib Isi)',
                'HARI\n(Rumus)'
            ]

            if PIC_COL in hasil.columns:
                kolom.append(PIC_COL)

            if 'Target' in hasil.columns:
                kolom.append('Target')

            st.dataframe(
                hasil[kolom],
                use_container_width=True
            )

# ==================================================
# MENU AM
# ==================================================
elif menu == "👤 Cari AM":

    st.subheader("👤 Cari Berdasarkan AM")

    am = st.text_input(
        "Masukkan Nama AM",
        placeholder="Contoh: MYA"
    )

    if am:

        hasil = df[
            df['AM\n(Rumus)']
            .astype(str)
            .str.upper()
            == am.upper()
        ]

        if hasil.empty:

            st.error("AM tidak ditemukan")

        else:

            st.success(
                f"Ditemukan {len(hasil)} event"
            )

            if 'Target' in hasil.columns:

                total_target = hitung_target(
                    hasil['Target']
                )

                st.metric(
                    "Total Target",
                    format_target(total_target)
                )

            kolom = [
                'KDTK\n(Wajib Isi)',
                'NAMA TOKO\n(Rumus)',
                'AS\n(Rumus)'
            ]

            if PIC_COL in hasil.columns:
                kolom.append(PIC_COL)

            kolom.append('TGL EVENT\n(Wajib Isi)')

            if 'Target' in hasil.columns:
                kolom.append('Target')

            st.dataframe(
                hasil[kolom],
                use_container_width=True
            )

# ==================================================
# MENU AS
# ==================================================
elif menu == "🧑‍💼 Cari AS":

    st.subheader("🧑‍💼 Cari Berdasarkan AS")

    as_input = st.text_input(
        "Masukkan Nama AS",
        placeholder="Contoh: MSI"
    )

    if as_input:

        hasil = df[
            df['AS\n(Rumus)']
            .astype(str)
            .str.upper()
            == as_input.upper()
        ]

        if hasil.empty:

            st.error("AS tidak ditemukan")

        else:

            st.success(
                f"Ditemukan {len(hasil)} event"
            )

            if 'Target' in hasil.columns:

                total_target = hitung_target(
                    hasil['Target']
                )

                st.metric(
                    "Total Target",
                    format_target(total_target)
                )

            kolom = [
                'KDTK\n(Wajib Isi)',
                'NAMA TOKO\n(Rumus)',
                'AM\n(Rumus)'
            ]

            if PIC_COL in hasil.columns:
                kolom.append(PIC_COL)

            kolom.append('TGL EVENT\n(Wajib Isi)')

            if 'Target' in hasil.columns:
                kolom.append('Target')

            st.dataframe(
                hasil[kolom],
                use_container_width=True
            )

# ==================================================
# MENU TANGGAL
# ==================================================
elif menu == "📅 Cari Tanggal":

    st.subheader("📅 Cari Berdasarkan Tanggal")

    tanggal = st.text_input(
        "Masukkan Tanggal Event",
        placeholder="Contoh: 7"
    )

    if tanggal:

        hasil = df[
            df['TGL EVENT\n(Wajib Isi)']
            .astype(str)
            .str.strip()
            == tanggal.strip()
        ]

        if hasil.empty:

            st.error(
                "Tidak ada event pada tanggal tersebut"
            )

        else:

            st.success(
                f"Ditemukan {len(hasil)} event"
            )

            if 'Target' in hasil.columns:

                total_target = hitung_target(
                    hasil['Target']
                )

                st.metric(
                    "Total Target Tanggal Ini",
                    format_target(total_target)
                )

            kolom = [
                'KDTK\n(Wajib Isi)',
                'NAMA TOKO\n(Rumus)',
                'AS\n(Rumus)',
                'AM\n(Rumus)'
            ]

            if PIC_COL in hasil.columns:
                kolom.append(PIC_COL)

            kolom.extend([
                'TGL EVENT\n(Wajib Isi)',
                'HARI\n(Rumus)'
            ])

            if 'Target' in hasil.columns:
                kolom.append('Target')

            st.dataframe(
                hasil[kolom],
                use_container_width=True
            )