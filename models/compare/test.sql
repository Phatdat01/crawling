{{ config(materialized='external', location="{{env_var('result_path')}}/COMPARE_ROUND4/RESULT_COMPARE_ROUND4.csv") }}
  WITH cl04_crm AS(
  SELECT 
    CONCAT_WS('',"Customer Payee", Promotion, "Customer Reference") as cl04_pk,
    "Customer Payee" as customer_payee, 
    Promotion as promotion,
    "Customer reference" as customer_reference,
    SUM(CAST(REPLACE("Value", ',', '') AS INTEGER)) AS value
    --SUM(cast("value" as Float)) AS value
  FROM {{source('duck_source','CL04_CRM')}}
  GROUP BY 1,2,3,4
  ),
  vn08_pr AS (
  SELECT 
    CONCAT_WS('',"ERPMã", PlanNumber, "Mã CTKM" ) AS vn08_pk,
    "ERPMã" AS erp_ma,
    PlanNumber AS plan_number,
    "Mã CTKM" AS ma_ctkm,
    ROUND(SUM(CAST("Số tiền KM" AS INTEGER )),0) AS so_tien_KM
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
*
FROM result
