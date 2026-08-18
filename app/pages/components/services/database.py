import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_database_connection():
    database_url = os.getenv("DATABASE_URL")

    connection = psycopg2.connect(database_url)

    return connection


def create_wedding(
    partner_1_name,
    partner_2_name,
    wedding_date,
    date_is_tbd,
    location,
    target_guest_count,
    target_budget,
    style_theme,
    wedding_website,
    cover_image_url,
    primary_color,
    secondary_color
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO weddings (
            partner_1_name,
            partner_2_name,
            wedding_date,
            date_is_tbd,
            location,
            target_guest_count,
            target_budget,
            style_theme,
            wedding_website,
            cover_image_url,
            primary_color,
            secondary_color
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING wedding_id;
        """,
        (
            partner_1_name,
            partner_2_name,
            wedding_date,
            date_is_tbd,
            location,
            target_guest_count,
            target_budget,
            style_theme,
            wedding_website,
            cover_image_url,
            primary_color,
            secondary_color
        )
    )

    wedding_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return wedding_id


def get_wedding(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            wedding_id,
            partner_1_name,
            partner_2_name,
            wedding_date,
            date_is_tbd,
            location,
            target_guest_count,
            target_budget,
            currency,
            style_theme,
            wedding_website,
            cover_image_url,
            primary_color,
            secondary_color,
            selected_venue_id
        FROM weddings
        WHERE wedding_id = %s;
        """,
        (wedding_id,)
    )

    wedding = cursor.fetchone()

    cursor.close()
    connection.close()

    return wedding


def update_wedding(
    wedding_id,
    partner_1_name,
    partner_2_name,
    wedding_date,
    date_is_tbd,
    location,
    target_guest_count,
    target_budget,
    style_theme,
    wedding_website,
    cover_image_url,
    primary_color,
    secondary_color
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE weddings
        SET
            partner_1_name = %s,
            partner_2_name = %s,
            wedding_date = %s,
            date_is_tbd = %s,
            location = %s,
            target_guest_count = %s,
            target_budget = %s,
            style_theme = %s,
            wedding_website = %s,
            cover_image_url = %s,
            primary_color = %s,
            secondary_color = %s,
            updated_at = NOW()
        WHERE wedding_id = %s;
        """,
        (
            partner_1_name,
            partner_2_name,
            wedding_date,
            date_is_tbd,
            location,
            target_guest_count,
            target_budget,
            style_theme,
            wedding_website,
            cover_image_url,
            primary_color,
            secondary_color,
            wedding_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def create_venue(
    wedding_id,
    venue_name,
    website,
    location,
    contact_name,
    contact_email,
    contact_phone,
    overall_capacity,
    availability_notes,
    curfew_time,
    insurance_requirements,
    notes,
    status
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO venues (
            wedding_id,
            venue_name,
            website,
            location,
            contact_name,
            contact_email,
            contact_phone,
            overall_capacity,
            availability_notes,
            curfew_time,
            insurance_requirements,
            notes,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING venue_id;
        """,
        (
            wedding_id,
            venue_name,
            website,
            location,
            contact_name,
            contact_email,
            contact_phone,
            overall_capacity,
            availability_notes,
            curfew_time,
            insurance_requirements,
            notes,
            status
        )
    )

    venue_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return venue_id


def get_venues(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            venue_id,
            venue_name,
            website,
            location,
            contact_name,
            contact_email,
            contact_phone,
            overall_capacity,
            availability_notes,
            curfew_time,
            insurance_requirements,
            notes,
            status
        FROM venues
        WHERE wedding_id = %s
        ORDER BY venue_name;
        """,
        (wedding_id,)
    )

    venues = cursor.fetchall()

    cursor.close()
    connection.close()

    return venues


def update_venue(
    venue_id,
    venue_name,
    website,
    location,
    contact_name,
    contact_email,
    contact_phone,
    overall_capacity,
    availability_notes,
    curfew_time,
    insurance_requirements,
    notes,
    status
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE venues
        SET
            venue_name = %s,
            website = %s,
            location = %s,
            contact_name = %s,
            contact_email = %s,
            contact_phone = %s,
            overall_capacity = %s,
            availability_notes = %s,
            curfew_time = %s,
            insurance_requirements = %s,
            notes = %s,
            status = %s,
            updated_at = NOW()
        WHERE venue_id = %s;
        """,
        (
            venue_name,
            website,
            location,
            contact_name,
            contact_email,
            contact_phone,
            overall_capacity,
            availability_notes,
            curfew_time,
            insurance_requirements,
            notes,
            status,
            venue_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def create_venue_package(
    venue_id,
    package_name,
    package_area,
    package_capacity,
    price,
    description,
    inclusions,
    exclusions,
    notes
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO venue_packages (
            venue_id,
            package_name,
            package_area,
            package_capacity,
            price,
            description,
            inclusions,
            exclusions,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING package_id;
        """,
        (
            venue_id,
            package_name,
            package_area,
            package_capacity,
            price,
            description,
            inclusions,
            exclusions,
            notes
        )
    )

    package_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return package_id


def get_venue_packages(venue_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            package_id,
            package_name,
            package_area,
            package_capacity,
            price,
            description,
            inclusions,
            exclusions,
            notes,
            is_selected
        FROM venue_packages
        WHERE venue_id = %s
        ORDER BY package_name;
        """,
        (venue_id,)
    )

    packages = cursor.fetchall()

    cursor.close()
    connection.close()

    return packages


def update_venue_package(
    package_id,
    package_name,
    package_area,
    package_capacity,
    price,
    description,
    inclusions,
    exclusions,
    notes
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE venue_packages
        SET
            package_name = %s,
            package_area = %s,
            package_capacity = %s,
            price = %s,
            description = %s,
            inclusions = %s,
            exclusions = %s,
            notes = %s,
            updated_at = NOW()
        WHERE package_id = %s;
        """,
        (
            package_name,
            package_area,
            package_capacity,
            price,
            description,
            inclusions,
            exclusions,
            notes,
            package_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def select_venue_package(wedding_id, venue_id, package_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE venue_packages
        SET is_selected = FALSE
        WHERE venue_id IN (
            SELECT venue_id
            FROM venues
            WHERE wedding_id = %s
        );
        """,
        (wedding_id,)
    )

    cursor.execute(
        """
        UPDATE venue_packages
        SET is_selected = TRUE
        WHERE package_id = %s;
        """,
        (package_id,)
    )

    cursor.execute(
        """
        UPDATE weddings
        SET
            selected_venue_id = %s,
            updated_at = NOW()
        WHERE wedding_id = %s;
        """,
        (venue_id, wedding_id)
    )

    connection.commit()
    cursor.close()
    connection.close()


def create_vendor(
    wedding_id,
    vendor_name,
    category,
    website,
    contact_name,
    contact_email,
    contact_phone,
    availability_notes,
    insurance_requirements,
    notes,
    status
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO vendors (
            wedding_id,
            vendor_name,
            category,
            website,
            contact_name,
            contact_email,
            contact_phone,
            availability_notes,
            insurance_requirements,
            notes,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING vendor_id;
        """,
        (
            wedding_id,
            vendor_name,
            category,
            website,
            contact_name,
            contact_email,
            contact_phone,
            availability_notes,
            insurance_requirements,
            notes,
            status
        )
    )

    vendor_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return vendor_id


def get_vendors(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            vendor_id,
            vendor_name,
            category,
            website,
            contact_name,
            contact_email,
            contact_phone,
            availability_notes,
            insurance_requirements,
            notes,
            status
        FROM vendors
        WHERE wedding_id = %s
        ORDER BY category, vendor_name;
        """,
        (wedding_id,)
    )

    vendors = cursor.fetchall()

    cursor.close()
    connection.close()

    return vendors


def update_vendor(
    vendor_id,
    vendor_name,
    category,
    website,
    contact_name,
    contact_email,
    contact_phone,
    availability_notes,
    insurance_requirements,
    notes,
    status
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE vendors
        SET
            vendor_name = %s,
            category = %s,
            website = %s,
            contact_name = %s,
            contact_email = %s,
            contact_phone = %s,
            availability_notes = %s,
            insurance_requirements = %s,
            notes = %s,
            status = %s,
            updated_at = NOW()
        WHERE vendor_id = %s;
        """,
        (
            vendor_name,
            category,
            website,
            contact_name,
            contact_email,
            contact_phone,
            availability_notes,
            insurance_requirements,
            notes,
            status,
            vendor_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def create_vendor_option(
    vendor_id,
    option_name,
    price,
    description,
    inclusions,
    exclusions,
    notes
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO vendor_options (
            vendor_id,
            option_name,
            price,
            description,
            inclusions,
            exclusions,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING option_id;
        """,
        (
            vendor_id,
            option_name,
            price,
            description,
            inclusions,
            exclusions,
            notes
        )
    )

    option_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return option_id


def get_vendor_options(vendor_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            option_id,
            option_name,
            price,
            description,
            inclusions,
            exclusions,
            notes,
            is_selected
        FROM vendor_options
        WHERE vendor_id = %s
        ORDER BY option_name;
        """,
        (vendor_id,)
    )

    options = cursor.fetchall()

    cursor.close()
    connection.close()

    return options


def update_vendor_option(
    option_id,
    option_name,
    price,
    description,
    inclusions,
    exclusions,
    notes
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE vendor_options
        SET
            option_name = %s,
            price = %s,
            description = %s,
            inclusions = %s,
            exclusions = %s,
            notes = %s,
            updated_at = NOW()
        WHERE option_id = %s;
        """,
        (
            option_name,
            price,
            description,
            inclusions,
            exclusions,
            notes,
            option_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def create_quote(
    vendor_id,
    option_id,
    quoted_price,
    quote_date,
    expiration_date,
    notes
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO quotes (
            vendor_id,
            option_id,
            quoted_price,
            quote_date,
            expiration_date,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING quote_id;
        """,
        (
            vendor_id,
            option_id,
            quoted_price,
            quote_date,
            expiration_date,
            notes
        )
    )

    quote_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return quote_id


def get_vendor_quotes(vendor_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            quote_id,
            option_id,
            quoted_price,
            quote_date,
            expiration_date,
            notes
        FROM quotes
        WHERE vendor_id = %s
        ORDER BY quote_date DESC;
        """,
        (vendor_id,)
    )

    quotes = cursor.fetchall()

    cursor.close()
    connection.close()

    return quotes


def select_vendor_option(wedding_id, vendor_id, option_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE vendor_options
        SET is_selected = FALSE
        WHERE vendor_id IN (
            SELECT vendor_id
            FROM vendors
            WHERE wedding_id = %s
        );
        """,
        (wedding_id,)
    )

    cursor.execute(
        """
        UPDATE vendor_options
        SET is_selected = TRUE
        WHERE option_id = %s;
        """,
        (option_id,)
    )

    cursor.execute(
        """
        UPDATE vendors
        SET
            status = CASE
                WHEN vendor_id = %s THEN 'Selected'
                ELSE status
            END,
            updated_at = NOW()
        WHERE wedding_id = %s;
        """,
        (vendor_id, wedding_id)
    )

    connection.commit()
    cursor.close()
    connection.close()


def create_milestone(
    wedding_id,
    title,
    category,
    target_date,
    status
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO milestones (
            wedding_id,
            title,
            category,
            target_date,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING milestone_id;
        """,
        (
            wedding_id,
            title,
            category,
            target_date,
            status
        )
    )

    milestone_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return milestone_id


def get_milestones(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            milestone_id,
            title,
            category,
            target_date,
            status,
            completed_date
        FROM milestones
        WHERE wedding_id = %s
        ORDER BY target_date;
        """,
        (wedding_id,)
    )

    milestones = cursor.fetchall()

    cursor.close()
    connection.close()

    return milestones


def create_task(
    wedding_id,
    milestone_id,
    title,
    description,
    category,
    due_date,
    priority,
    status,
    assigned_user_id
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (
            wedding_id,
            milestone_id,
            title,
            description,
            category,
            due_date,
            priority,
            status,
            assigned_user_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING task_id;
        """,
        (
            wedding_id,
            milestone_id,
            title,
            description,
            category,
            due_date,
            priority,
            status,
            assigned_user_id
        )
    )

    task_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return task_id


def get_tasks(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            task_id,
            milestone_id,
            title,
            description,
            category,
            due_date,
            priority,
            status,
            assigned_user_id,
            completed_date
        FROM tasks
        WHERE wedding_id = %s
        ORDER BY due_date;
        """,
        (wedding_id,)
    )

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return tasks


def update_task_status(task_id, status):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET
            status = %s,
            completed_date = CASE
                WHEN %s = 'Complete' THEN CURRENT_DATE
                ELSE NULL
            END,
            updated_at = NOW()
        WHERE task_id = %s;
        """,
        (
            status,
            status,
            task_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def create_budget_category(
    wedding_id,
    category_name,
    allocated_amount
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO budget_categories (
            wedding_id,
            category_name,
            allocated_amount
        )
        VALUES (%s, %s, %s)
        RETURNING budget_category_id;
        """,
        (
            wedding_id,
            category_name,
            allocated_amount
        )
    )

    budget_category_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return budget_category_id


def get_budget_categories(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            budget_category_id,
            category_name,
            allocated_amount
        FROM budget_categories
        WHERE wedding_id = %s
        ORDER BY category_name;
        """,
        (wedding_id,)
    )

    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return categories


def create_payment(
    contract_id,
    amount,
    due_date,
    paid_date,
    status,
    payment_type,
    notes
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO payments (
            contract_id,
            amount,
            due_date,
            paid_date,
            status,
            payment_type,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING payment_id;
        """,
        (
            contract_id,
            amount,
            due_date,
            paid_date,
            status,
            payment_type,
            notes
        )
    )

    payment_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return payment_id


def get_contract_payments(contract_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            payment_id,
            amount,
            due_date,
            paid_date,
            status,
            payment_type,
            notes
        FROM payments
        WHERE contract_id = %s
        ORDER BY due_date;
        """,
        (contract_id,)
    )

    payments = cursor.fetchall()

    cursor.close()
    connection.close()

    return payments

def create_procurement_item(
    wedding_id,
    item_name,
    category,
    quantity,
    needed_by_date,
    estimated_unit_cost,
    actual_unit_cost,
    supplier_name,
    lead_time_days,
    shipping_days,
    safety_buffer_days,
    status,
    notes
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO procurement_items (
            wedding_id,
            item_name,
            category,
            quantity,
            needed_by_date,
            estimated_unit_cost,
            actual_unit_cost,
            supplier_name,
            lead_time_days,
            shipping_days,
            safety_buffer_days,
            status,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING procurement_item_id;
        """,
        (
            wedding_id,
            item_name,
            category,
            quantity,
            needed_by_date,
            estimated_unit_cost,
            actual_unit_cost,
            supplier_name,
            lead_time_days,
            shipping_days,
            safety_buffer_days,
            status,
            notes
        )
    )

    procurement_item_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return procurement_item_id


def get_procurement_items(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            procurement_item_id,
            item_name,
            category,
            quantity,
            needed_by_date,
            estimated_unit_cost,
            actual_unit_cost,
            supplier_name,
            lead_time_days,
            shipping_days,
            safety_buffer_days,
            status,
            notes
        FROM procurement_items
        WHERE wedding_id = %s
        ORDER BY needed_by_date;
        """,
        (wedding_id,)
    )

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return items

def create_guest(
    wedding_id,
    household_id,
    first_name,
    last_name,
    email,
    phone,
    invited,
    save_the_date_sent,
    invitation_sent,
    rsvp_status,
    rsvp_date,
    plus_one_allowed,
    meal_selection,
    dietary_allergies,
    thank_you_sent
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO guests (
            wedding_id,
            household_id,
            first_name,
            last_name,
            email,
            phone,
            invited,
            save_the_date_sent,
            invitation_sent,
            rsvp_status,
            rsvp_date,
            plus_one_allowed,
            meal_selection,
            dietary_allergies,
            thank_you_sent
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING guest_id;
        """,
        (
            wedding_id,
            household_id,
            first_name,
            last_name,
            email,
            phone,
            invited,
            save_the_date_sent,
            invitation_sent,
            rsvp_status,
            rsvp_date,
            plus_one_allowed,
            meal_selection,
            dietary_allergies,
            thank_you_sent
        )
    )

    guest_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return guest_id


def get_guests(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            guest_id,
            household_id,
            first_name,
            last_name,
            email,
            phone,
            invited,
            save_the_date_sent,
            invitation_sent,
            rsvp_status,
            rsvp_date,
            plus_one_allowed,
            meal_selection,
            dietary_allergies,
            thank_you_sent,
            seating_table_id,
            hotel_id,
            arrival_date,
            departure_date,
            transportation_needed,
            travel_notes
        FROM guests
        WHERE wedding_id = %s
        ORDER BY last_name, first_name;
        """,
        (wedding_id,)
    )

    guests = cursor.fetchall()

    cursor.close()
    connection.close()

    return guests

def create_document(
    wedding_id,
    file_name,
    file_type,
    document_type,
    storage_path,
    uploaded_by,
    venue_id,
    vendor_id,
    contract_id,
    payment_id,
    procurement_item_id
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents (
            wedding_id,
            file_name,
            file_type,
            document_type,
            storage_path,
            uploaded_by,
            venue_id,
            vendor_id,
            contract_id,
            payment_id,
            procurement_item_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING document_id;
        """,
        (
            wedding_id,
            file_name,
            file_type,
            document_type,
            storage_path,
            uploaded_by,
            venue_id,
            vendor_id,
            contract_id,
            payment_id,
            procurement_item_id
        )
    )

    document_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return document_id


def get_documents(wedding_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            document_id,
            file_name,
            file_type,
            document_type,
            storage_path,
            uploaded_by,
            uploaded_at,
            venue_id,
            vendor_id,
            contract_id,
            payment_id,
            procurement_item_id
        FROM documents
        WHERE wedding_id = %s
        ORDER BY uploaded_at DESC;
        """,
        (wedding_id,)
    )

    documents = cursor.fetchall()

    cursor.close()
    connection.close()

    return documents



