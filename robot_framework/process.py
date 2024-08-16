"""This module contains the main process of the robot."""
import os
import json

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from itk_dev_shared_components.sap import sap_login, multi_session

from robot_framework.subprocesses.sap_create_invoice import InvoiceHandler


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")

    orchestrator_connection.log_trace("Open SAP.")
    creds_sap = orchestrator_connection.get_credential("sap_kostordning")
    sap_login.login_using_cli(username=creds_sap.username, password=creds_sap.password, client='751', system='P02', timeout=60)

    orchestrator_connection.log_trace("Get SAP sessions.")
    sessions = multi_session.get_all_sap_sessions()
    first_session = sessions[0]

    orchestrator_connection.log_trace("Create invoice.")
    oc_args_json = json.loads(orchestrator_connection.process_arguments)
    transaction_code = oc_args_json['transactionCode']
    first_session.StartTransaction(transaction_code)

    invoice_creator = InvoiceHandler(first_session)
    invoice_creator.create_invoice(
        business_partner_id="",
        content_type="",
        base_system_id="",
        name_person="",
        start_date="",
        end_date="",
        institution_number="",
        main_transaction_id="",
        main_transaction_amount="",
        sub_transaction_id="",
        sub_transaction_fee_adm_id="",
        sub_transaction_fee_adm_amount="",
        sub_transaction_fee_inst_id="",
        sub_transaction_fee_inst_amount="",
        payment_recipient_identifier="",
        service_recipient_identifier=""
    )


if __name__ == "__main__":
    oc = OrchestratorConnection('Process name', os.getenv('OpenOrchestratorConnString'), os.getenv('OpenOrchestratorKey'), '{"transactionCode":"zdkd_opret_faktura"}')
    process(oc)
