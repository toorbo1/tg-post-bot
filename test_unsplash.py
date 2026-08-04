import requests
ids = [
    "1518770660439-4636190af475", "1498050105-c83b4eef52a5",
    "1504384308090-c894fdcc538d", "1451187580459-43490279c0fa",
    "1531297484001-80022131f5a1", "1526374965328-7f61d4dc18c5",
    "1558346490-a72e53ae2d4f", "1550751827-4bd374c3f58b",
    "1563986768609-322da13575f2", "1486312338219-ce68d2c6f44d",
    "1558494946-45c92c78e5cd", "1544191696-465a2d2a2171",
    "1461749280684-dccba630e2f6", "1504639725590-34d0984388bd",
    "1527477390581-5e3bf0d0a0b0", "1555949963-ff9fe0c870eb",
    "1534664637627-3c42bafe7c78", "1515876427279-3c5e2c271683",
    "1504868581-c0b12be0b3f8", "1536147111177-68c0835161d2",
    "1519389950473-47ba0277781c", "1473090805000-9ab7b99f533b",
    "1510555619082-66fc2eb782f5", "1517245386807-bb43f82c33c4",
    "1551288049-bebda4e38f71", "1460925895917-afdab827c52f",
    "1507003211169-0a1dd7228f2d", "1423666639041-fce3847da0e8",
    "1471105160404c6f35f7b48e", "1462896876630-1d6b1c1b3b2c",
    "1497366216548-375a7024c7b0", "1484419413010-2a8f6c997c8f",
    "1497366815962-0e2f45d6e7b1", "1476954075237-27f7bc34b9b0",
    "1504293856366-7b9b6d8df7e8", "1517245386807-bb43f82c33c4",
    "1542744094-24638f0c66af", "1551288049-bebda4e38f71",
    "1433160491599-3a76c6b4e9c", "1485827404703-89b55fcc595e",
]
ok = []
for pid in ids:
    url = f"https://images.unsplash.com/photo-{pid}?w=1200&auto=format"
    try:
        r = requests.head(url, allow_redirects=True, timeout=5)
        if r.status_code == 200:
            ok.append("photo-" + pid)
            print("OK: photo-" + pid)
        else:
            print("FAIL(" + str(r.status_code) + "): photo-" + pid)
    except Exception as e:
        print("ERR: photo-" + pid + " " + str(e)[:40])
print("\nWorking IDs (" + str(len(ok)) + "):")
for o in ok:
    print('    "' + o + '",')
