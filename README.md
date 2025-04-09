# EC2 설정 
1. Computing : T2 micro 성능 낮아도 충분히 작동 
2. OS : AWS Linux 아무거나
3. 크롬 버전 : 133.05.m


# 실행
python3 LH.py \
  --s3_bucket your-bucket-name \
  --s3_key_prefix "lh-notices" \
  --aws_access_key YOUR_ACCESS_KEY \
  --aws_secret_key YOUR_SECRET_KEY \
  --aws_region ap-northeast-2
