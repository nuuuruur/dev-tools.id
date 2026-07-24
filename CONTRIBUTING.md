# Contributing

## Cara Menambah Tool

1. Buka file YAML yang sesuai di folder `data/` (misal `data/hosting_murah.yaml`)
2. Tambah entry baru di bagian `items:`:

```yaml
- name: Nama Service
  url: https://example.com
  tried: false
  notes:
    - text: "Keterangan singkat"
      author: "github_username"
```

3. Jalankan generator untuk update README:

Pastikan sudah install package (Pyyaml)[https://pypi.org/project/PyYAML/]
```bash
python3 generate.py
```

Jika ada URL yang sudah ada di file lain, generator akan memberi tahu dan menolak generate. Hapus entry duplikat dulu.

4. Commit perubahan di `data/*.yaml` DAN `README.md`

## Field

| Field    | Wajib | Keterangan |
|----------|-------|------------|
| `name`   | Ya    | Nama service |
| `url`    | Ya    | URL website |
| `tried`  | Ya    | `true` jika sudah dicoba, `false` jika belum |
| `notes`  | Tidak | List catatan dari kontributor (lihat format di bawah) |

### Format Notes

Notes berupa list, setiap item punya `text` dan `author` (GitHub username). Avatar contributor akan otomatis ditampilkan di README.

```yaml
notes:
  - text: "Harga murah tapi support lambat"
    author: "username_anda"
  - text: "Sudah saya coba, works great"
    author: "kontributor_lain"
```

Jika tidak ada author, cukup isi `author: ""` atau gunakan format lama (string biasa).

## Menambah Kategori Baru

1. Buat file baru di `data/` (misal `data/database_service.yaml`)
2. Gunakan format:

```yaml
title: "Nama Kategori"
disclaimer: "Disclaimer untuk kategori ini"
note: "Catatan opsional untuk kategori ini"
items:
  - name: ...
```

3. Jalankan `python3 generate.py`

## Template
```yaml
- name: 
  url: 
  tried: 
  notes:
    - text: ""
      author: ""
```
