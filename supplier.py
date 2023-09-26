import utils

def supplierExpirations():
    """Identify suppliers that have expired and send email to appropriate people."""
    
    sql = "select s.SUPPLIER_ID, s.NAME, q.EXPIRY_DATE from SUPPLIER s left join SUPPLIER_QMS q on s.SUPPLIER_ID = q.SUPPLIER_ID where (EXPIRY_DATE < NOW() or EXPIRY_DATE is null) and s.STATUS = 'A';"
    
    expiredSuppliers = utils.getDatabaseData(sql)
    expiredSuppliersDisplay = "Expired suppliers: \n" + str(expiredSuppliers) + "\n"
    # print(expiredSuppliersDisplay)
    for supplierid, name, expdate in expiredSuppliers:
        notification = '''This supplier's qms expired on %s. Please review and take appropriate action. \nSupplier id: %s, name: %s''' % (expdate, supplierid, name)
        asstoemail = "tim.kent@ci-aviation.com"
        # utils.sendMail(to_email=[asstoemail], subject=f"Corrective Action Issued: {corrid}", message=notification, cc_email=["tim.kent@ci-aviation.com"])
        utils.sendMail(to_email=[asstoemail], subject=f"Supplier reapproval", message=notification)
        # print(notification)


def main():
    supplierExpirations()


if __name__ == '__main__':
    main()
    print("Done.")