import time
import asyncio
import logging
import statistics
import base64
from typing import Dict
from tabulate import tabulate
from core.utils.vllm import create_instance
from config.settings import load_config

# Set the global log level to WARNING and suppress INFO level logs
logging.basicConfig(level=logging.WARNING)

description = "Visual recognition model performance test"


class AsyncVisionPerformanceTester:
    def __init__(self):
        self.config = load_config()

        self.test_images = [
            "../../docs/images/demo1.png",
            "../../docs/images/demo2.png",
        ]
        self.test_questions = [
            "What's in this picture?",
            "Please describe the content of this image in detail",
        ]

        # Load test image
        self.results = {"vllm": {}}

    async def _test_vllm(self, vllm_name: str, config: Dict) -> Dict:
        """Asynchronously test the performance of a single visual large model"""
        try:
            # Check API key configuration
            if "api_key" in config and any(
                x in config["api_key"] for x in ["your", "placeholder", "sk-xxx"]
            ):
                print(f"⏭️ VLLM {vllm_name} is not configured with api_key and has been skipped")
                return {"name": vllm_name, "type": "vllm", "errors": 1}

            # Get the actual type (compatible with old configurations)
            module_type = config.get("type", vllm_name)
            vllm = create_instance(module_type, config)

            print(f"🖼️ Test VLLM: {vllm_name}")

            # Create all test tasks
            test_tasks = []
            for question in self.test_questions:
                for image in self.test_images:
                    test_tasks.append(
                        self._test_single_vision(vllm_name, vllm, question, image)
                    )

            # Execute all tests concurrently
            test_results = await asyncio.gather(*test_tasks)

            # Processing results
            valid_results = [r for r in test_results if r is not None]
            if not valid_results:
                print(f"⚠️ {vllm_name} has no valid data and may be configured incorrectly")
                return {"name": vllm_name, "type": "vllm", "errors": 1}

            response_times = [r["response_time"] for r in valid_results]

            # Filter abnormal data
            mean = statistics.mean(response_times)
            stdev = statistics.stdev(response_times) if len(response_times) > 1 else 0
            filtered_times = [t for t in response_times if t <= mean + 3 * stdev]

            if len(filtered_times) < len(test_tasks) * 0.5:
                print(f"⚠️ {vllm_name} Insufficient valid data, the network may be unstable")
                return {"name": vllm_name, "type": "vllm", "errors": 1}

            return {
                "name": vllm_name,
                "type": "vllm",
                "avg_response": sum(response_times) / len(response_times),
                "std_response": (
                    statistics.stdev(response_times) if len(response_times) > 1 else 0
                ),
                "errors": 0,
            }

        except Exception as e:
            print(f"⚠️ VLLM {vllm_name} test failed: {str(e)}")
            return {"name": vllm_name, "type": "vllm", "errors": 1}

    async def _test_single_vision(
        self, vllm_name: str, vllm, question: str, image: str
    ) -> Dict:
        """Test performance on a single vision problem"""
        try:
            print(f"📝 {vllm_name} Start testing: {question[:20]}...")
            start_time = time.time()

            # Read the image and convert to base64
            with open(image, "rb") as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode("utf-8")

            # Get response directly
            response = vllm.response(question, image_base64)
            response_time = time.time() - start_time
            print(f"✓ {vllm_name} completed response: {response_time:.3f}s")

            return {
                "name": vllm_name,
                "type": "vllm",
                "response_time": response_time,
            }
        except Exception as e:
            print(f"⚠️ {vllm_name} test failed: {str(e)}")
            return None

    def _print_results(self):
        """Print test results"""
        vllm_table = []
        for name, data in self.results["vllm"].items():
            if data["errors"] == 0:
                stability = data["std_response"] / data["avg_response"]
                vllm_table.append(
                    [
                        name,
                        f"{data['avg_response']:.3f} seconds",
                        f"{stability:.3f}",
                    ]
                )

        if vllm_table:
            print("\nVisual large model performance ranking:\n")
            print(
                tabulate(
                    vllm_table,
                    headers=["Model name", "Response time", "stability"],
                    tablefmt="github",
                    colalign=("left", "right", "right"),
                    disable_numparse=True,
                )
            )
        else:
            print("\n⚠️ No large visual model available for testing.")

    async def run(self):
        """Execute full asynchronous testing"""
        print("🔍 Start filtering available visual models...")

        if not self.test_images:
            print(f"\n⚠️ There is no image file in the {self.image_root} path and cannot be tested.")
            return

        # Create all test tasks
        all_tasks = []

        # VLLM test tasks
        if self.config.get("VLLM") is not None:
            for vllm_name, config in self.config.get("VLLM", {}).items():
                if "api_key" in config and any(
                    x in config["api_key"] for x in ["your", "placeholder", "sk-xxx"]
                ):
                    print(f"⏭️ VLLM {vllm_name} is not configured with api_key and has been skipped")
                    continue
                print(f"🖼️ Add VLLM test task: {vllm_name}")
                all_tasks.append(self._test_vllm(vllm_name, config))

        print(f"\n✅ Found {len(all_tasks)} available visual models")
        print(f"✅ Use {len(self.test_images)} test images")
        print(f"✅ Use {len(self.test_questions)} test questions")
        print("\n⏳ Start testing all models concurrently...\n")

        # Execute all test tasks concurrently
        all_results = await asyncio.gather(*all_tasks, return_exceptions=True)

        # Processing results
        for result in all_results:
            if isinstance(result, dict) and result["errors"] == 0:
                self.results["vllm"][result["name"]] = result

        # Print results
        print("\n📊 Generate test report...")
        self._print_results()


async def main():
    tester = AsyncVisionPerformanceTester()
    await tester.run()


if __name__ == "__main__":
    asyncio.run(main())
