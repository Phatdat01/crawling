{{ config(materialized='external', location="{{env_var('result_path')}}/COMPARE_ROUND5/RESULT_COMPARE_ROUND5.csv") }}
WITH cl02_pro AS (
  SELECT
  "Program_ID" as ma_chuong_trinh_khuyen_mai,
  CAST(REPLACE("Total",',','') AS FLOAT) AS thanh_tien
  FROM {{source('duck_source','CL02_PROMOTION_CLAIM_FOC')}}
),
vn08_pr AS (
  SELECT 
    "Program_ID" AS ma_ctkm,
    ROUND(SUM(CAST("Amount" AS FLOAT)),0) AS so_tien_km
  FROM {{source('duck_source','VN08_DIST_PROMOTION')}}
  GROUP BY 1
),
result AS (
SELECT 
  cl02_pro.ma_chuong_trinh_khuyen_mai,
  cl02_pro.thanh_tien, 
  vn08_pr.ma_ctkm,
  vn08_pr.so_tien_km,
  cl02_pro.thanh_tien - vn08_pr.so_tien_km as GAP
FROM cl02_pro
FULL JOIN vn08_pr
ON cl02_pro.ma_chuong_trinh_khuyen_mai = vn08_pr.ma_ctkm
)
SELECT 
  *,
  CASE 
    WHEN GAP = 0 THEN 'Match'
    WHEN GAP !=0 THEN 'Not Match'
    WHEN ma_chuong_trinh_khuyen_mai IS NULL AND ma_ctkm IS NULL THEN 'Both are NULL'
    WHEN ma_chuong_trinh_khuyen_mai IS NULL THEN 'Value in CL02 is Null'
    WHEN ma_ctkm IS NULL THEN 'Value in VN08 is Null'
  END AS status
FROM result