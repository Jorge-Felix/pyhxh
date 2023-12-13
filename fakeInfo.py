from faker import Faker
import sys
from colorama import Fore,Style

fake = Faker()


info={
    "Name: ": fake.name(),
    "Direction: ": fake.address(),
    "Email: ": fake.free_email(),
    "Phone Number: ": fake.phone_number(),
    "Passport Number: ": fake.passport_number(),
    "Date Of Birth: ": str(fake.date_of_birth()),
    "Company: ": fake.company(),
    "Job: ": fake.job(),
    "Credit card: ":fake.credit_card_full(),
    "Iban number: ": fake.iban(),
    "Bank Account Number: ": fake.bban(),
    "Username: ": fake.user_name(),
    "IPv4: ": fake.ipv4(),
    "uuid4: ": fake.uuid4()
}

for _,value in info.items():
    sys.stdout.write(str(Fore.BLUE + _ + Style.RESET_ALL))
    sys.stdout.write(str(Fore.RED + value + Style.RESET_ALL + '\n\n'))