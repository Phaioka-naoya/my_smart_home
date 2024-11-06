import configparser
import json
from switchbot_controller import SwitchBotController
import logging

def main():
    """メイン実行関数"""
    # ログの設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        # 設定値
        TOKEN = "51f25102c4cbca86f418c4d30e14634c297effad946043f9f541b2396cca6f6f0b1c45f4c4b471849c18b07594fed14c"
        SECRET = "13c1768ee91a4b36330881486e853648"
        DEVICE_ID = "6055F92BA2E2"  # DeskLight
        
        # コントローラーのインスタンス化
        controller = SwitchBotController(TOKEN, SECRET)

         # コマンドの実行
        #result = controller.send_device_command(DEVICE_ID, "toggle")
        #result = controller.send_device_command(DEVICE_ID, "setColorTemperature",500)
        #result = controller.get_device_status(DEVICE_ID)
        #result = controller.get_device_list()

        
        # デバイスの状態を取得
        device_status = controller.get_device_status(DEVICE_ID)
        logger.info(f"デバイス状態: {json.dumps(device_status, indent=2)}")

        if device_status["statusCode"] == 100:
            power_state = device_status["body"]["power"]  # 正しいJSONパス
            
            if power_state == "on":
                controller.send_device_command(DEVICE_ID, "setBrightness",40)
                result = controller.send_device_command(DEVICE_ID, "setColorTemperature",3000)
                logger.info("デバイスはON状態です")
            else:
                logger.info("デバイスはOFF状態です")
        else:
            logger.warning(f"デバイス状態の取得に失敗: {result['message']}")
            
    except KeyError as e:
        logger.error(f"JSONデータの構造が不正ですよ: {str(e)}")
    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()