from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['/home/samiksha889/project/config_manager/config/cloud.yaml'],
)

def main():
    print("provider:", settings.cloud_details.sample_domain.provider)
    print("Region:", settings.cloud_details.sample_domain.region)

main()