import requests
import json
import time
import hashlib
import hmac
import base64
import uuid
import logging

"""
External References:
    - SwitchBot Official API Documentation
      URL: https://github.com/OpenWonderLabs/SwitchBotAPI
      Version: 1.1 (Accessed: 2024/11)
      Description: Official API documentation for SwitchBot device integration
"""


class SwitchBotController:
    def __init__(self, token, secret):
        """初期化"""
        self.token = token
        self.secret = secret
        self.base_url = "https://api.switch-bot.com/v1.1"
        
        # ログの設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _generate_headers(self):
        """認証ヘッダーを生成"""
        try:
            nonce = uuid.uuid4()
            t = int(round(time.time() * 1000))
            
            # 署名文字列の作成
            string_to_sign = '{}{}{}'.format(self.token, t, nonce)
            string_to_sign = bytes(string_to_sign, 'utf-8')
            secret = bytes(self.secret, 'utf-8')
            
            # 署名の生成
            sign = base64.b64encode(
                hmac.new(secret, 
                        msg=string_to_sign, 
                        digestmod=hashlib.sha256).digest()
            )
            
            # ヘッダーの構築
            headers = {
                'Authorization': self.token,
                'Content-Type': 'application/json',
                'charset': 'utf8',
                't': str(t),
                'sign': str(sign, 'utf-8'),
                'nonce': str(nonce)
            }
            
            return headers
            
        except Exception as e:
            self.logger.error(f"ヘッダー生成エラー: {str(e)}")
            raise

    def send_device_command(self, device_id, command, parameter="default"):
        """デバイスにコマンドを送信"""
        try:
            # エンドポイントURLの構築
            url = f"{self.base_url}/devices/{device_id}/commands"
            
            # ヘッダーの取得
            headers = self._generate_headers()
            
            # ペイロードの構築
            payload = {
                "command": command,
                "parameter": parameter,
                "commandType": "command"
            }
            
            # リクエストの実行
            self.logger.info(f"コマンド送信: {device_id} - {command}")
            response = requests.post(url, headers=headers, json=payload)
            
            # レスポンスの確認
            response.raise_for_status()
            
            self.logger.info(f"コマンド成功: {response.json()}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API実行エラー: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"予期せぬエラー: {str(e)}")
            raise

    def get_device_status(self, device_id):
        """デバイスの状態を取得"""
        url = f"{self.base_url}/devices/{device_id}/status"
        headers = self._generate_headers()
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_device_list(self):
        """デバイスリストを取得"""
        try:
            url = f"{self.base_url}/devices"
            headers = self._generate_headers()
            
            self.logger.info("デバイスリスト取得開始")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"デバイスリスト取得成功: {len(data.get('body', {}).get('deviceList', []))}台のデバイスを検出")
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"デバイスリスト取得エラー: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"予期せぬエラー: {str(e)}")
            raise