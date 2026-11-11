from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 生成符合新 UI 需求的知识库构建结果数据
def generate_knowledge_base_results():
    # 1. 参数特征数据 (左侧表格)
    parameters = [
        {"name": "PV出力波动", "mean": "0.75", "variance": "0.12", "trend": "+8.5%", "confidence": "92%"},
        {"name": "负荷需求", "mean": "1.23", "variance": "0.25", "trend": "-3.2%", "confidence": "88%"},
        {"name": "储能SOC", "mean": "0.60", "variance": "0.08", "trend": "稳定", "confidence": "95%"},
        {"name": "天气影响因子", "mean": "0.45", "variance": "0.18", "trend": "+12%", "confidence": "78%"},
        {"name": "故障持续因子", "mean": "1.25", "variance": "0.45", "trend": "稳定", "confidence": "91%"},
        {"name": "电压波动幅度", "mean": "0.08", "variance": "0.03", "trend": "+6%", "confidence": "94%"}
    ]

    # 2. 场景统计数据 (右上表格)
    scenarios = [
        {"name": "电压跌落场景", "count": 5},
        {"name": "过负荷场景", "count": 8},
        {"name": "孤岛场景", "count": 3},
        {"name": "极端天气场景", "count": 6}
    ]

    # 3. 汇总数据 (右下表格)
    # 自动生成当前时间作为最后更新时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {
        "total_samples": "12,845条",
        "new_samples": "126条/小时",
        "kb_confidence": "94.5%",
        "last_update": current_time
    }

    return parameters, scenarios, summary

@app.route('/run_matlab', methods=['GET', 'POST'])
def get_knowledge_graph_data():
    try:
        # 接收前端可能传来的参数 (如果有的话)
        if request.method == 'POST':
            # 预留接收数据输入的接口 (历史负荷、光伏出力等)
            req_data = request.get_json()
            logging.info(f"收到前端数据输入: {req_data}")

        # 调用生成逻辑
        parameters, scenarios, summary = generate_knowledge_base_results()

        # 构建符合前端新 UI 的 JSON payload
        frontend_payload = {
            "status": "success",
            "message": "事故动态知识库构建结果更新成功",
            "data": {
                "parameter_features": parameters,
                "scenario_statistics": scenarios,
                "summary_statistics": summary
            }
        }
        return jsonify(frontend_payload), 200

    except Exception as e:
        logging.error(f"知识库构建失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5026, debug=False)
