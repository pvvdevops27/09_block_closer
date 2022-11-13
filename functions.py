from functions_library import gsheet_to_df, df_to_gsheet, move_drive_file, logger


def block_approver():

    # # Pending approval dataframe
    df = gsheet_to_df("1L5mPhKxdJahnC8arqDBwl5FZWKcyroZZd3HEw2XODlQ",
                      "Block in progress")

    # Exceptions

    # Companies that were not approved will raise an exception.

    if len(df[df['approvalStatus'] == ""]["approvalStatus"]) == 0:
        print("Success. All companies were approved")

    else:
        raise Exception("Failure. Some companies require attention")

    if len(df[df['reason'] == ""]["reason"]) == 0:
        print("Companies were approved succesfully")

    else:
        raise Exception(
            "Some approvals were made incorrecly. Check empty reason cells")

    # Writing into approvedPool

    columns = ["cif",
               "niche",
               "name",
               "charge",
               "web",
               "contactName",
               "linkedin",
               "email",
               "phone",
               "fullAddress",
               "connectionLinkedinDate",
               "connectionEmailDate",
               "connectionPhoneDate",
               "connectionAddressDate",
               "responseLinkedinDate",
               "responseEmailDate",
               "responsePhoneDate",
               "responseAddressDate",
               "actionType",
               "reason",
               "actionPhoneFrequency",
               "approvalStatus"]

    df_to_gsheet("12B1RyjGdWob34ZZ0jYy6h6mEfuQba1GS7A8Mwxx5pdY",
                 "approvedPool", df, columns=columns)

    # Move approved block to Approved blocks
    move_drive_file(
        source_folder_id="1bXmKcohGYpjeKv-mQ_PA5-bOo927vnRb", target_folder_id="1Tz4cOH1MxAm7jn_lGumVdJ7QChbDLWWY", name="Beta")

    # Logs writting

    logger("Block approver")
