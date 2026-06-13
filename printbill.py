from db import load_config
import win32print
import win32ui
import win32con
from datetime import datetime


def check_printer(printer_name):
    hprinter = None
    try:
        hprinter = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(hprinter, 2)
        status = printer_info["Status"]

        if status != 0:
            raise Exception(f"Printer is not ready. Status code: {status}")

    except Exception as e:
        raise Exception(f"Printer check failed: {e}") from e

    finally:
        if hprinter:
            win32print.ClosePrinter(hprinter)


def build_header(patient_name, clinic_name):
    now = datetime.now().strftime("%d-%m-%Y  %H:%M")
    lines = []
    lines.append("================================")
    lines.append(f"        {clinic_name}")
    lines.append("       PHARMACY BILL")
    lines.append("================================")
    lines.append(f" Date   : {now}")
    lines.append(f" Patient: {patient_name}")
    lines.append("================================")
    lines.append(f" {'Medicine':<16} {'Qty':<5} {'Price':<10} {'Total'}")
    lines.append("--------------------------------")
    return lines


def build_body(bill_items):
    lines = []
    for name, qty, unit_price, total in bill_items:
        lines.append(f" {name:<16} {qty:<5} Rs.{unit_price:<7.2f} Rs.{total:.2f}")
    return lines


def build_footer(grand_total, clinic_name):
    lines = []
    lines.append("--------------------------------")
    lines.append(f" Grand Total:       Rs.{grand_total:.2f}")
    lines.append("================================")
    lines.append("   Thank you for visiting!")
    lines.append(f"        {clinic_name}")
    lines.append("================================")
    return lines


def build_patient_header(patient_name, doctor_name, clinic_name):
    now = datetime.now().strftime("%d-%m-%Y  %H:%M")
    lines = []
    lines.append("================================")
    lines.append(f"        {clinic_name}")
    lines.append("         PATIENT BILL")
    lines.append("================================")
    lines.append(f" Date   : {now}")
    lines.append(f" Patient: {patient_name}")
    lines.append(f" Doctor : {doctor_name}")
    lines.append("================================")
    lines.append(f" {'Medicine':<16} {'Qty':<5} {'Price':<10} {'Total'}")
    lines.append("--------------------------------")
    return lines


def build_patient_footer(medicine_total, doctor_charges, grand_total, clinic_name):
    lines = []
    lines.append("--------------------------------")
    lines.append(f" Medicine Total:    Rs.{medicine_total:.2f}")
    lines.append(f" Doctor Charges:    Rs.{doctor_charges:.2f}")
    lines.append("--------------------------------")
    lines.append(f" Grand Total:       Rs.{grand_total:.2f}")
    lines.append("================================")
    lines.append("   Thank you for visiting!")
    lines.append(f"        {clinic_name}")
    lines.append("================================")
    return lines


def print_patient_bill(patient_name, doctor_name, bill_items, medicine_total, doctor_charges, grand_total):
    config = load_config()
    printer_name = config["printer_name"]
    clinic_name  = config["clinic_name"]

    try:
        check_printer(printer_name)
    except Exception as e:
        print(f"Cannot print: {e}")
        return

    lines = []
    lines += build_patient_header(patient_name, doctor_name, clinic_name)
    lines += build_body(bill_items)
    lines += build_patient_footer(medicine_total, doctor_charges, grand_total, clinic_name)

    dc = win32ui.CreateDC()
    dc.CreatePrinterDC(printer_name)
    dc.StartDoc("Patient Bill")

    try:
        dc.StartPage()

        font = win32ui.CreateFont({
            "name": "Courier New",
            "height": -16,
            "weight": win32con.FW_NORMAL,
            "charset": win32con.ANSI_CHARSET,
        })
        dc.SelectObject(font)

        x = 10
        y = 10
        line_height = 20

        for line in lines:
            dc.TextOut(x, y, line)
            y += line_height

        dc.EndPage()
        dc.EndDoc()

    except Exception as e:
        print(f"Printing failed: {e}")

    finally:
        dc.DeleteDC()


def print_bill(patient_name, bill_items, grand_total):
    config = load_config()
    printer_name = config["printer_name"]
    clinic_name  = config["clinic_name"]

    # ── Check printer before doing anything ─────────────────────
    try:
        check_printer(printer_name)
    except Exception as e:
        print(f"Cannot print: {e}")
        return

    # ── Build all sections ───────────────────────────────────────
    lines = []
    lines += build_header(patient_name, clinic_name)
    lines += build_body(bill_items)
    lines += build_footer(grand_total, clinic_name)

    # ── Print via GDI ────────────────────────────────────────────
    dc = win32ui.CreateDC()
    dc.CreatePrinterDC(printer_name)
    dc.StartDoc("Medicine Bill")

    try:
        dc.StartPage()

        font = win32ui.CreateFont({
            "name": "Courier New",
            "height": -16,
            "weight": win32con.FW_NORMAL,
            "charset": win32con.ANSI_CHARSET,
        })
        dc.SelectObject(font)

        x = 10
        y = 10
        line_height = 20

        for line in lines:
            dc.TextOut(x, y, line)
            y += line_height

        dc.EndPage()
        dc.EndDoc()

    except Exception as e:
        print(f"Printing failed: {e}")

    finally:
        dc.DeleteDC()