import re

def record_types():
    valid_record_types = [
        "A", "AAAA", "CNAME", "MX", "TXT",
        "PTR", "SRV", "SPF", "NAPTR", "CAA",
        "DS", "TLSA", "SSHFP", "HTTPS", "SVCB"
    ]
    record_type = input("Enter record type (A, CNAME, MX, TXT, AAAA): ").upper()
    while record_type not in valid_record_types:
        print("Invalid record type. Please enter 'A', 'AAAA', 'CNAME', 'MX', 'TXT', 'PTR', 'SRV', 'SPF', 'NAPTR', 'CAA', 'DS', 'TLSA', 'SSHFP', 'HTTPS', or 'SVCB'.")
        record_type = input("Enter record type (A, CNAME, MX, TXT, AAAA): ").upper()

    return record_type

def record_type_A(record_value):
    while not re.match(r"^\d+\.\d+\.\d+\.\d+$", record_value):
        print(f"Invalid record value for 'A' record: {record_value}. Please enter a valid IPv4 address.")
        print("Example of a valid 'A' record: 192.168.1.1")
    return record_value


def record_type_AAAA(record_value):
    while not re.match(r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$", record_value):
        print(f"Invalid record value for 'AAAA' record: {record_value}. Please enter a valid IPv6 address.")
        print("Example of a valid 'AAAA' record: 2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    return record_value


def record_type_CNAME(record_value):
    while not re.match(r"^[a-zA-Z0-9.-]+\.$", record_value):
        print(f"Invalid record value for 'CNAME' record: {record_value}. Please enter a valid domain name (FQDN).")
        print("Example of a valid 'CNAME' record: www.example.com.")
    return record_value


def record_type_MX(record_value):
    parts = record_value.split(" ")
    while len(parts) != 2 or not parts[0].isdigit() or not re.match(r"^[a-zA-Z0-9.-]+\.$", parts[1]):
        print(
            f"Invalid record value for 'MX' record: {record_value}. Please enter a valid priority and mail server domain.")
        print("Example of a valid 'MX' record: 10 mail.example.com.")
    return record_value


def record_type_TXT(record_value):
    while len(record_value) > 255:
        print(f"TXT record value is too long. Maximum length allowed is 255 characters.")
        print("Example of a valid 'TXT' record: \"v=spf1 include:_spf.google.com ~all\"")
    return record_value


def record_type_PTR(record_value):
    while not re.match(r"^[a-zA-Z0-9.-]+\.$", record_value):
        print(f"Invalid record value for 'PTR' record: {record_value}. Please enter a valid PTR domain name.")
        print("Example of a valid 'PTR' record: example.com.")
    return record_value


def record_type_SRV(record_value):
    parts = record_value.split(" ")
    while len(parts) != 4 or not parts[0].isdigit() or not parts[1].isdigit() or not parts[2].isdigit() or not re.match(
            r"^[a-zA-Z0-9.-]+\.$", parts[3]):
        print(
            f"Invalid record value for 'SRV' record: {record_value}. Please enter a valid priority, weight, port, and target.")
        print("Example of a valid 'SRV' record: 10 5 5060 sip.example.com.")
    return record_value


def record_type_SPF(record_value):
    while len(record_value) > 255:
        print(f"SPF record value is too long. Maximum length allowed is 255 characters.")
        print("Example of a valid 'SPF' record: v=spf1 include:_spf.google.com ~all")
    while not re.match(r"^v=spf1 .*", record_value):
        print(f"Invalid SPF record value: {record_value}. Must begin with 'v=spf1'.")
    return record_value


def record_type_NAPTR(record_value):
    parts = record_value.split(" ")
    while len(parts) != 6:
        print(f"Invalid record value for 'NAPTR' record: {record_value}. Expected 6 parts.")
        print("Example of a valid 'NAPTR' record: 100 10 \"U\" \"E2U+sip\" \"!^.*$!sip:example.com!\" .")
        return
    while parts:
        if not parts[0].isdigit():
            print(f"Invalid order in 'NAPTR' record: {parts[0]}. Must be an integer.")
        if not parts[1].isdigit():
            print(f"Invalid preference in 'NAPTR' record: {parts[1]}. Must be an integer.")
        if not re.match(r"^[A-Za-z0-9]+$", parts[2]):
            print(f"Invalid flags in 'NAPTR' record: {parts[2]}. Must be alphanumeric.")
        if not re.match(r"^[A-Za-z0-9+/.-]+$", parts[3]):
            print(f"Invalid service in 'NAPTR' record: {parts[3]}. Must be a valid service name.")
        if not re.match(r"^/.*/$", parts[4]):
            print(f"Invalid regexp in 'NAPTR' record: {parts[4]}. Must be a valid regular expression wrapped in slashes.")
        if not re.match(r"^[a-zA-Z0-9.-]+\.$", parts[5]):
            print(f"Invalid replacement in 'NAPTR' record: {parts[5]}. Must be a valid domain name.")
        else:
            break
    return record_value


def record_type_CAA(record_value):
    while len(record_value.split(" ")) != 3:
        print(f"Invalid record value for 'CAA' record: {record_value}. Please enter valid flags, tag, and value.")
        print("Example of a valid 'CAA' record: 0 issue \"letsencrypt.org\"")
        record_value=input("Enter record value: ")

    parts = record_value.split(" ")
    while parts:
        if not parts[0].isdigit() or not re.match(r"^[a-zA-Z0-9-]+$", parts[1]) or not re.match(r"^[a-zA-Z0-9.-]+$",                                                                          parts[2]):
            print(f"Invalid record value for 'CAA' record: {record_value}. Please enter valid flags, tag, and value.")
            record_value = input("Enter record value: ")

    return record_value


def record_type_DS(record_value):
    parts = record_value.split(" ")
    while len(parts) != 4 or not parts[0].isdigit() or not parts[1].isdigit() or not parts[2].isdigit() or not re.match(
            r"^[A-F0-9]+$", parts[3]):
        print(
            f"Invalid record value for 'DS' record: {record_value}. Please enter valid key tag, algorithm, digest type, and digest.")
        print(
            "Example of a valid 'DS' record: 12345 2 1 59f3507e387b736a99098f79fbc5f16c2cfadf798db645919f819fa33a15b7b9")
        record_value=input("Enter record value: ")

    return record_value


def record_type_TLSA(record_value):
    parts = record_value.split(" ")
    while len(parts) != 4 or not parts[0].isdigit() or not parts[1].isdigit() or not parts[2].isdigit() or not re.match(
            r"^[A-F0-9]+$", parts[3]):
        print(
            f"Invalid record value for 'TLSA' record: {record_value}. Please enter valid usage, selector, matching type, and certificate association data.")
        print(
            "Example of a valid 'TLSA' record: 3 1 1 59f3507e387b736a99098f79fbc5f16c2cfadf798db645919f819fa33a15b7b9")
        record_value=input("Enter record value: ")

    return record_value


def record_type_SSHFP(record_value):
    parts = record_value.split(" ")
    if len(parts) != 3 or not parts[0].isdigit() or not re.match(r"^[A-F0-9]+$", parts[1]) or not re.match(
            r"^[A-F0-9]+$", parts[2]):
        print(
            f"Invalid record value for 'SSHFP' record: {record_value}. Please enter valid algorithm, fingerprint type, and fingerprint.")
        print("Example of a valid 'SSHFP' record: 1 2 59f3507e387b736a99098f79fbc5f16c2cfadf798db645919f819fa33a15b7b9")
        record_value=input("Enter record value: ")

    return record_value


def record_type_HTTPS(record_value):
    if not re.match(r"^[a-zA-Z0-9.-]+\.$", record_value):
        print(f"Invalid record value for 'HTTPS' record: {record_value}. Please enter a valid HTTPS record format.")
        print("Example of a valid 'HTTPS' record: _https.example.com.")
        record_value=input("Enter record value: ")

    return record_value


def record_type_SVCB(record_value):
    while not re.match(r"^[a-zA-Z0-9.-]+\.$", record_value):
        print(f"Invalid record value for 'SVCB' record: {record_value}. Please enter a valid domain name.")
        print("Example of a valid 'SVCB' record: _svc.example.com.")
        record_value=input("Enter record value: ")
    return record_value

def record_types_conditions(record_type,record_value):
    if record_type == "A":
        record_value=record_type_A(record_value)
    elif record_type == "AAAA":
        record_value=record_type_AAAA(record_value)
    elif record_type == "CNAME":
        record_value=record_type_CNAME(record_value)
    elif record_type == "MX":
        record_value=record_type_MX(record_value)
    elif record_type == "TXT":
        record_value=record_type_TXT(record_value)
    elif record_type == "PTR":
        record_value=record_type_PTR(record_value)
    elif record_type == "SRV":
        record_value=record_type_SRV(record_value)
    elif record_type == "SPF":
        record_value=record_type_SPF(record_value)
    elif record_type == "NAPTR":
        record_value=record_type_NAPTR(record_value)
    elif record_type == "CAA":
        record_value=record_type_CAA(record_value)
    elif record_type == "DS":
        record_value=record_type_DS(record_value)
    elif record_type == "TLSA":
        record_value=record_type_TLSA(record_value)
    elif record_type == "SSHFP":
        record_value=record_type_SSHFP(record_value)
    elif record_type == "HTTPS":
        record_value=record_type_HTTPS(record_value)
    elif record_type == "SVCB":
        record_value=record_type_SVCB(record_value)

    return record_value


def valid_ttl():
    ttl = int(input("Enter TTL (between 60 and 86400 seconds): "))
    while ttl < 60 or ttl > 86400 :
        print("Invalid TTL value. It must be an integer between 60 and 86400.")
        ttl = int(input("Enter TTL (between 60 and 86400 seconds): "))
    return ttl

