import csv
import pprint as pp


def csv_to_json():
    containers = []
    with open("all_containers.csv") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if check_row_for_cve(row):
                # Build dictiorary with the VulnerabilityID being the main key
                packages = {}
                containers.append(build_dict(row, packages))
    return containers


def build_dict(row, p_info):
    package = row[2]
    if package not in p_info:
        p_info["package"] = set()
        p_info["package"].add(row[0])  # package name

        p_info["package_path"] = set()
        p_info["package_path"].add(row[1])  # package path

        p_info["severity"] = set()
        p_info["severity"].add(row[3])  # severity

        p_info["installed_versions"] = set()
        p_info["installed_versions"].add(row[4])  # installed versions

        p_info["fixed_versions"] = set()
        p_info["fixed_versions"].add(row[5])  # fixed versions

        p_info["links"] = set()
        p_info["links"].add(row[6])  # links
    else:
        p_info = p_info[package]
        p_info["package"].add(row[0])  # package name
        p_info["package_path"].add(row[1])  # package path
        p_info["severity"].add(row[3])  # severity
        p_info["installed_versions"].add(row[4])  # installed versions
        p_info["fixed_versions"].add(row[5])  # fixed versions
        p_info["links"].add(row[6])  # links
    return p_info


# If the row has a CVE then is can be formatted
def check_row_for_cve(row):
    for cve in row:
        if "CVE" in cve:
            return True
    return False


if __name__ == '__main__':
    pp.pp(csv_to_json())