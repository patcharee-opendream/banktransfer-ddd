from sqlalchemy.orm import registry, composite
from sqlalchemy import (
    Table,
    Column,
    Integer,
    MetaData,
    String,
    JSON,
    Enum,
    DateTime,
    BIGINT,
)
from modules.bank_transfer_donation.domain.aggregate.model import (
    BankTransferDonation,
    BankTransferStatus,
)


from modules.donee.domain.value_objects import Donee, DoneeType
from modules.donor.domain.value_objects import Donor, DonorType


metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def start_mapper():
    # create table
    table = Table(
        "bank_transfer_donation",
        metadata,
        Column("id", BIGINT, primary_key=True),
        Column("donation_number", String),
        Column("version", Integer),
        Column("created_at", DateTime(timezone=True)),
        Column("updated_at", String),
        Column("donor_type", Enum(DonorType)),
        Column("donor_email", String),
        Column("donor_phone", String),
        Column("donor_name1", String),
        Column("donor_name2", String),
        Column("donor_name_prefix", String),
        Column("donor_tax_id", String),
        Column("donee_ref_id", Integer),
        Column("donee_type", Enum(DoneeType)),
        Column("donee_name", String),
        Column("expected_amount", String),
        Column("currency", String),
        Column("status", Enum(BankTransferStatus)),
        Column("donation_created_at", String),
        Column("donee_meta", JSON),
        Column("donor_member_id", String),
        Column("meta", JSON),
    )

    mapper_registry.map_imperatively(
        BankTransferDonation,
        table,
        properties={
            "donor": composite(
                Donor,
                table.c.donor_type,
                table.c.donor_email,
                table.c.donor_phone,
                table.c.donor_name1,
                table.c.donor_name2,
                table.c.donor_name_prefix,
                table.c.donor_tax_id,
                table.c.donor_member_id,
            ),
            "donee": composite(
                Donee,
                table.c.donee_ref_id,
                table.c.donee_name,
                table.c.donee_type,
                table.c.donee_meta,
            ),
        },
    )
