{{config(materialized = 'external', location = "{{env_var('result_path')}}/COMPARE_ROUND7/RESULT_COMPARE_ROUND7.csv")}}
WITH invoice_dtl AS (
  SELECT 
      Region as region, 
      SUM(CAST("Gross Amount" AS float)) AS gross_amount
  FROM {{source('duck_source','INVOICE_DTL')}}
  group by Region
),

txn_noteprd_cp AS (
  SELECT 
    Region as region, 
    SUM(CAST("Gross Amount" AS float)) AS gross_amount
  FROM {{source('duck_source','TXN_NOTEPRD_CP')}}
  GROUP BY Region
),

secondary_sales_GSV AS (
  SELECT 
    Region as region, 
    ROUND(SUM(CAST("GSV_AmountWithTax" AS FLOAT)),0) AS gsv_amount_withtax
  FROM {{source('duck_source','VN01_SECONDARY_SALES_GSV')}}
  GROUP BY region
),
combine_invoice_dtl_and_txn_noteprd_cp as (
  SELECT
  invoice_dtl.region,
  invoice_dtl.gross_amount as gross_amount_dtl,
  COALESCE(txn_noteprd_cp.gross_amount, 0) as gross_amount_prd
  FROM invoice_dtl
  FULL JOIN txn_noteprd_cp 
ON invoice_dtl.region = txn_noteprd_cp.region
)
SELECT 
	combine_invoice_dtl_and_txn_noteprd_cp.region,
	combine_invoice_dtl_and_txn_noteprd_cp.gross_amount_dtl,
	combine_invoice_dtl_and_txn_noteprd_cp.gross_amount_prd,
	secondary_sales_GSV.gsv_amount_withtax,
	secondary_sales_GSV.gsv_amount_withtax - (combine_invoice_dtl_and_txn_noteprd_cp.gross_amount_dtl - combine_invoice_dtl_and_txn_noteprd_cp.gross_amount_prd) as GAP
FROM combine_invoice_dtl_and_txn_noteprd_cp
FULL OUTER JOIN secondary_sales_GSV
ON combine_invoice_dtl_and_txn_noteprd_cp.region = secondary_sales_GSV.region