import configparser
import json
from switchbot_controller import SwitchBotController
import logging

def main():
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
        result = controller.send_device_command(DEVICE_ID, "toggle")

    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()