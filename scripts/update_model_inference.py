import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    inference_data = {
        "id": "concept_model_inference",
        "title": "Model Inference & Serving",
        "topic_id": "ml_linear",
        "topic_label": "Linear Regression & Core ML Concepts",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Inference / Prediction (Computing y' from new inputs)",
        "def": "Model inference is using an already-trained model with fixed weights to make predictions, while model serving is hosting that model through an API so other applications can request those predictions.",
        "formula": "$$\\hat{y} = f(\\mathbf{x}_{\\text{new}}; \\; \\mathbf{w}^*, b^*) \\quad \\xrightarrow{\\text{REST / gRPC API}} \\quad \\text{JSON Response} \\quad (\\text{Latency } < 50\\text{ms})$$",
        "logic": "Training takes hours or days to calculate the best weights. Once training is complete, the weights are locked in place. Inference simply multiplies incoming new features by those frozen weights to output an instant prediction in milliseconds.",
        "example": "Ride-share fare estimate: When you open Uber and type your destination, the app sends your trip features to a FastAPI server. In 15 milliseconds, the frozen model calculates the price ($24.50) and returns it to your phone screen.",
        "tags": [
            "Inference",
            "Model Serving",
            "Production ML",
            "FastAPI",
            "Latency",
            "ONNX"
        ],
        "definition": "Model inference is using an already-trained model with fixed weights to make predictions, while model serving is hosting that model through an API so other applications can request those predictions.",
        "formula_explanation": "",
        "simple_summary": "Training is when the model studies the textbook; inference is when it takes the test. During inference, model weights are frozen and never change. Serving means putting that model inside a web service (like FastAPI or Docker) so apps, websites, or phones can send in new questions and receive instant answers in under 50 milliseconds.",
        "core_terms": [
            {
                "term": "Model Inference",
                "what_is_it": "• The process of feeding brand-new, unseen inputs into an already-trained model to get a prediction.\n• The model's weights are completely frozen; no learning or parameter updates occur.",
                "analogy": "Using a finished calculator: you type in 5 + 5 and get 10; the calculator doesn't change how it does math.",
                "why_it_matters": "Inference is where a model delivers real business value to users after training is finished."
            },
            {
                "term": "Model Serving",
                "what_is_it": "• Wrapping the trained model inside a web service (like FastAPI or Flask) so other software can call it.\n• Handles incoming requests, validates inputs, runs inference, and returns a JSON response.",
                "analogy": "A restaurant waiter: taking orders from dining tables, bringing them to the kitchen, and serving back the finished food.",
                "why_it_matters": "A trained model sitting in a Jupyter Notebook is useless until it is served to live applications."
            },
            {
                "term": "Quantization & ONNX Runtime",
                "what_is_it": "• Production speedup techniques that shrink model weights from 32-bit decimals down to 8-bit integers.\n• Compiles models so they run in fast C++ engines without needing Python or heavy PyTorch libraries.",
                "analogy": "Compressing a huge video into an MP4 file that plays smoothly on any phone without lagging.",
                "why_it_matters": "Shrinks model memory by 75% and speeds up predictions by 2x to 4x with virtually zero loss in accuracy."
            }
        ],
        "types_header": "The 3 Production Serving Paradigms",
        "types_badge": "Architecture Patterns",
        "quick_types": [
            {
                "type": "Online / Real-Time Serving",
                "definition": "Returns predictions instantly over a REST or gRPC API; ideal for credit card fraud checks and live search.",
                "looks_like": "Latency: < 50 ms (e.g., FastAPI + Docker)"
            },
            {
                "type": "Batch / Offline Serving",
                "definition": "Scores millions of records together on a schedule; ideal for nightly customer churn reports.",
                "looks_like": "Latency: Hours/Days (e.g., Nightly Spark SQL job)"
            },
            {
                "type": "Edge / On-Device Serving",
                "definition": "Runs directly on the user's phone or hardware with zero network lag and total user privacy.",
                "looks_like": "Latency: < 5 ms (e.g., Apple FaceID, CoreML, TFLite)"
            },
            {
                "type": "Microservice Container (Docker)",
                "definition": "Packages the model, code, and exact dependencies into a portable container that runs anywhere.",
                "looks_like": "docker run -p 8000:8000 ml-serving-api"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "x_new",
                "meaning": "Live Production Input",
                "plain_english": "Brand-new feature values sent by a user or application"
            },
            {
                "symbol": "w*, b*",
                "meaning": "Frozen Parameters",
                "plain_english": "The fixed weights and bias saved during training that never change during inference"
            },
            {
                "symbol": "p99 Latency",
                "meaning": "99th Percentile Response Time",
                "plain_english": "The maximum time taken by 99% of requests (a standard SLA is p99 < 50ms)"
            },
            {
                "symbol": "QPS",
                "meaning": "Queries Per Second (Throughput)",
                "plain_english": "How many prediction requests the server can handle every second"
            }
        ],
        "numerical_example": "Production Serving Request Lifecycle:\n\nStep 1: Application Request (Time = 0 ms)\n• User clicks 'Apply for Loan' on a bank website.\n• Frontend sends JSON payload: {'income': 85000, 'credit_score': 720, 'debt': 12000}\n\nStep 2: API Validation & Preprocessing (Time = 3 ms)\n• FastAPI validates inputs using Pydantic.\n• Saved StandardScaler transforms raw values into normalized numbers.\n\nStep 3: Model Inference (Time = 7 ms)\n• Pre-loaded frozen weights evaluate the formula in memory: ŷ = σ(w^T x + b) = 0.94 (Approval probability: 94%).\n\nStep 4: Response Delivery (Time = 12 ms total)\n• API returns response: {'approved': True, 'confidence': 0.94}\n• SLA Met: Total round-trip latency of 12 ms is well within the 50 ms budget!",
        "pitfalls": "Common Pitfall: Loading the model file on every single HTTP request. If your API loads model.pkl from disk each time a user calls the endpoint, response times jump from 10ms to over 2 seconds! Always load your model once into memory when the server starts up (e.g., inside FastAPI's lifespan event). Also, watch out for preprocessing skew: always save your scaler, encoder, and model together inside a single Pipeline so live inference applies the exact same transformations as training.",
        "core_logic": "Why this matters: Training is compute-heavy and only happens occasionally (weekly or monthly). Inference is latency-critical and happens constantly (thousands of times every second). In production engineering, saving 20 milliseconds of latency or reducing server memory directly cuts cloud infrastructure bills and keeps users happy.",
        "architectural_logic": "In modern production systems, models are converted to ONNX or TensorRT format and served using dedicated inference servers like Triton Inference Server or TorchServe. These engines support dynamic batching, pooling multiple concurrent incoming user requests into a single matrix calculation on the GPU.",
        "connected_logic": [
            {
                "title": "Online vs Batch vs Edge Trade-offs",
                "content": "• Online Serving: Instant answers, but requires dedicated 24/7 web servers with high uptime.\n• Batch Serving: Cheap and highly scalable on huge datasets, but predictions are not available in real-time.\n• Edge Serving: Zero network latency and private, but limited by phone battery and hardware power."
            },
            {
                "title": "The Training-Serving Skew Danger",
                "content": "• If training clipped outliers to 100 but the serving API receives 500 without clipping, predictions will be wildly wrong.\n• Exporting an end-to-end pipeline ensures raw data goes in and final predictions come out with zero manual glue code."
            },
            {
                "title": "Quantization: Shrinking Models for Production",
                "content": "• Converting 32-bit floats to 8-bit integers (int8) reduces memory footprints by 75%.\n• Modern CPUs and mobile chips have dedicated int8 hardware instructions that double inference speeds."
            },
            {
                "title": "Security: Untrusted Pickle and Joblib Files",
                "content": "• Python pickle files can execute arbitrary malicious operating system commands during deserialization.\n• Never load pickle or Joblib models from unknown third parties; use safer formats like Safetensors or ONNX."
            }
        ],
        "key_takeaways": [
            "Training vs Inference: Training learns weights; inference uses frozen weights to make instant predictions.",
            "Serving Paradigms: Choose Online for live apps (<50ms), Batch for daily bulk reports, and Edge for phones.",
            "Load Once: Load model objects into memory at server startup, never inside the request handler.",
            "Optimize with Quantization: Use 8-bit quantization and ONNX runtime to reduce latency and cloud costs."
        ],
        "definition_bullets": [
            "Model Inference: Using a trained model with frozen parameters to compute predictions on new input data.",
            "Model Serving: Exposing an inference pipeline through an accessible network service such as a REST API."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_model_inference":
            c.update(inference_data)
            print("Updated concept_model_inference in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_model_inference":
            c.update(inference_data)
            print("Updated concept_model_inference in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_model_inference".*?\},(?=\s*\{\s*"id":\s*"concept_squared_loss")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(inference_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_model_inference in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
