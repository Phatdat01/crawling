{{ config(materialized='external', location="{{env_var('result_path')}}/COMPARE_ROUND4/RESULT_COMPARE_ROUND4.csv") }}
  WITH cl04_crm AS(
  SELECT 
    CONCAT_WS('',"CustomerPayee", Promotion, "CustomerReference",'_',"ClaimDescription") as cl04_pk,
    "CustomerPayee" as customer_payee, 
    Promotion as promotion,
    "CustomerReference" as customer_reference,
    SUM(CAST(REPLACE("Value", ',', '') AS INTEGER)) AS value
    --SUM(cast("value" as Float)) AS value
  FROM {{source('duck_source','CL04_CRM')}}
  GROUP BY 1,2,3,4
  ),
  vn08_pr AS (
  SELECT 
    CONCAT_WS('',"ERPCode", PlanNumber, "PromotionProgram" ) AS vn08_pk,
    "ERPCode" AS erp_ma,
    PlanNumber AS plan_number,
    "PromotionProgram" AS ma_ctkm,
    ROUND(SUM(CAST("Amount" AS INTEGER )),0) AS so_tien_KM
  FROM {{source('duck_source','VN08_DIST_PROMOTION')}}
  GROUP BY 1,2,3,4
  ),
result AS (
SELECT 
  cl04.cl04_pk,
  cl04.customer_payee, 
  cl04.promotion,
  cl04.customer_reference,
  cl04.value,
  vn08.vn08_pk,
  vn08.erp_ma,
  vn08.plan_number,
  vn08.ma_ctkm,
  vn08.so_tien_KM,
  cl04.value - vn08.so_tien_KM as GAP
FROM cl04_crm AS cl04
FULL JOIN vn08_pr AS vn08
ON cl04.cl04_pk = vn08.vn08_pk 
)
SELECT 
  customer_payee, 
  promotion,
  customer_reference,
  value,
  erp_ma,
  plan_number,
  ma_ctkm,
  so_tien_KM,
  GAP,
  CASE 
		WHEN GAP = 0 THEN 'Match'
		WHEN GAP !=0 THEN 'Not Match'
    WHEN cl04_pk IS NULL AND vn08_pk IS NULL THEN 'Both are NULL'
		WHEN cl04_pk IS NULL THEN 'Value in CL04 is Null'
		WHEN vn08_pk IS NULL THEN 'Value in VN08 is Null'
	END AS status
FROM result