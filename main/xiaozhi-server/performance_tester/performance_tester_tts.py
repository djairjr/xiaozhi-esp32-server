import asyncio
import logging
import os
import time
from typing import Dict
import yaml
from tabulate import tabulate

# Make sure to import create_tts_instance from core.utils.tts
from core.utils.tts import create_instance as create_tts_instance
from config.settings import load_config

# Set global log level to WARNING
logging.basicConfig(level=logging.WARNING)

description = "Non-streaming speech synthesis performance test"


class TTSPerformanceTester:
    def __init__(self):
        self.config = load_config()
        self.test_sentences = self.config.get("module_test", {}).get(
            "test_sentences",
            [
                "In the ninth year of Yonghe, he was in Guichou, at the beginning of late spring;",
                "The lady's relationship with her will last a lifetime, or she may be held in her arms and enlightened within a room; or she may wander away from home because of her entrustment. Although there are many different interests, calmness and restlessness are different,",
                "Every time I look at the reasons for people's interest in the past, if they are combined into one, I will not fail to express my condolences in writing, which cannot be expressed in my heart. I know that death and rebirth are just illusions, and mourning for Qi Peng is an illusion.",
            ],
        )
        self.results = {}

    async def _test_tts(self, tts_name: str, config: Dict) -> Dict:
        """Test the performance of a single TTS module"""
        try:
            token_fields = ["access_token", "api_key", "token"]
            if any(
                field in config
                and any(x in config[field] for x in ["your", "placeholder"])
                for field in token_fields
            ):
                print(f"TTS {tts_name} is not configured with access_token/api_key and has been skipped")
                return {"name": tts_name, "errors": 1}

            module_type = config.get("type", tts_name)
            tts = create_tts_instance(module_type, config, delete_audio_file=True)

            print(f"Test TTS: {tts_name}")

            # Connection test
            tmp_file = tts.generate_filename()
            await tts.text_to_speak("Connection test", tmp_file)

            if not tmp_file or not os.path.exists(tmp_file):
                print(f"{tts_name} connection failed")
                return {"name": tts_name, "errors": 1}

            total_time = 0
            test_count = len(self.test_sentences[:3])

            for i, sentence in enumerate(self.test_sentences[:2], 1):
                start = time.time()
                tmp_file = tts.generate_filename()
                await tts.text_to_speak(sentence, tmp_file)
                duration = time.time() - start
                total_time += duration

                if tmp_file and os.path.exists(tmp_file):
                    print(f"{tts_name} [{i}/{test_count}] Test successful")
                else:
                    print(f"{tts_name} [{i}/{test_count}] test failed")
                    return {"name": tts_name, "errors": 1}

            return {
                "name": tts_name,
                "avg_time": total_time / test_count,
                "errors": 0,
            }

        except Exception as e:
            print(f"{tts_name} test failed: {str(e)}")
            return {"name": tts_name, "errors": 1}

    def _print_results(self):
        """Print test results"""
        if not self.results:
            print("No valid TTS test results")
            return

        headers = ["TTS module", "Average time taken (seconds)", "Number of test sentences", "state"]
        table_data = []

        # Collect all data and categorize it
        valid_results = []
        error_results = []

        for name, data in self.results.items():
            if data["errors"] == 0:
                # normal result
                avg_time = f"{data['avg_time']:.3f}"
                test_count = len(self.test_sentences[:3])
                status = "✅Normal"
                
                # Save the value used for sorting
                valid_results.append({
                    "name": name,
                    "avg_time": avg_time,
                    "test_count": test_count,
                    "status": status,
                    "sort_key": data['avg_time']
                })
            else:
                # Wrong result
                avg_time = "-"
                test_count = "0/3"
                
                # The default error type is network error
                error_type = "network error"
                status = f"❌ {error_type}"
                
                error_results.append([name, avg_time, test_count, status])

        # Sort by average time in ascending order
        valid_results.sort(key=lambda x: x["sort_key"])

        # Convert the sorted valid results into tabular data
        for result in valid_results:
            table_data.append([
                result["name"],
                result["avg_time"],
                result["test_count"],
                result["status"]
            ])

        # Add error results to the end of table data
        table_data.extend(error_results)

        print("\nTTS performance test results:")
        print(
            tabulate(
                table_data,
                headers=headers,
                tablefmt="grid",
                colalign=("left", "right", "right", "left"),
            )
        )
        print("\nTest description:")
        print("- Timeout control: The maximum waiting time for a single request is 10 seconds")
        print("- Error handling: Unable to connect and timeout are listed as network errors")
        print("- Sorting rules: Sort by average time consumption from fastest to slowest")

    async def run(self):
        """Execute tests"""
        print("Start TTS performance test...")

        if not self.config.get("TTS"):
            print("TTS configuration not found in configuration file")
            return

        # Traverse all TTS configurations
        tasks = []
        for tts_name, config in self.config.get("TTS", {}).items():
            tasks.append(self._test_tts(tts_name, config))

        # Execute tests concurrently
        results = await asyncio.gather(*tasks)

        # Save all results, including errors
        for result in results:
            self.results[result["name"]] = result

        # Print results
        self._print_results()


# For the calling requirements of performance_tester.py
async def main():
    tester = TTSPerformanceTester()
    await tester.run()


if __name__ == "__main__":
    tester = TTSPerformanceTester()
    asyncio.run(tester.run())
