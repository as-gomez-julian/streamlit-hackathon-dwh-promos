MAIN_QUERY = """--sql
SELECT
  country_name,
  retailer_name,
  store_key,
  master_store_id,
  store_name,
  full_date,
  category_name,
  product_name,
  ean_sku_code,
  product_promo_price,
  is_promo_price,
  product_other_promotions,
  is_other_promo
FROM
  `prod-shelftia-as.flattening_data.dw_hktn_promos`
"""