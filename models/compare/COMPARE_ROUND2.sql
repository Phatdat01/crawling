{{ config(materialized='external', location="{{env_var('result_path')}}/COMPARE_ROUND2/RESULT_COMPARE_ROUND2.csv") }}
WITH invoice_hdr AS
(
	SELECT 
		CONCAT("Distributor Code",'|',"Invoice No") AS pk , 
		"Distributor Code" as distributor_code, 
		"Invoice No" as invoice_no, 
		"Gross Amount (After SKU disc)" as gross_amount_after_sku_disc 
	FROM {{source('duck_source','INVOICE_HDR')}}
),
txn_notehdr_cp AS
(
	SELECT 
		CONCAT("Distributor Code",'|',"Invoice No") AS pk, 
		"Distributor Code" as distributor_code, 
		"Invoice No" as invoice_no, 
		"Total Amount (After SKU Discount)" as total_amount_after_sku_discount
	FROM {{source('duck_source','TXN_NOTEHDR_CP')}}
),
check_gap AS (
	SELECT 
		invoice_hdr.pk AS invoice_hdr_pk,
		txn_notehdr_cp.pk AS notehdr_pk,
		invoice_hdr.distributor_code AS invoice_distributor_code,
		invoice_hdr.invoice_no AS invoice_invoice_no,
		invoice_hdr.gross_amount_after_sku_disc,
		txn_notehdr_cp.distributor_code AS notehdr_distributor_code,
		txn_notehdr_cp.invoice_no AS notehdr_invoice_no,
		txn_notehdr_cp.total_amount_after_sku_discount,
		txn_notehdr_cp.total_amount_after_sku_discount - invoice_hdr.gross_amount_after_sku_disc AS GAP
	FROM invoice_hdr 
	FULL OUTER JOIN txn_notehdr_cp
	ON invoice_hdr.distributor_code = txn_notehdr_cp.distributor_code
	AND invoice_hdr.invoice_no = txn_notehdr_cp.invoice_no
)
SELECT 
	invoice_distributor_code,
	invoice_invoice_no,
	gross_amount_after_sku_disc,
	notehdr_distributor_code,
	notehdr_invoice_no,
	total_amount_after_sku_discount,
	GAP,
	CASE 
		WHEN GAP = 0 THEN 'Match'
		WHEN GAP !=0 THEN 'Not Match'
   		WHEN invoice_hdr_pk IS NULL AND notehdr_pk IS NULL THEN 'Both are NULL'
		WHEN invoice_hdr_pk IS NULL THEN 'Value in InvoiceDTL is Null'
		WHEN notehdr_pk IS NULL THEN 'Value in NoteHDR is Null'
	END AS status
FROM check_gap
