import argparse
import logging
import threading
from queue import Queue

from scripts.image_generator.generate import generate
from scripts.image_generator.generation_parameters import (
    Dimensions,
    GenerationParameters,
)

logging.basicConfig(level=logging.INFO)


def parse_args(args_list):
    parser = argparse.ArgumentParser(description="A-Eye Image Generator CLI")
    parser.add_argument(
        "--image",
        type=str,
        help="File name or file path of the base image.",
        required=True,
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="The positive prompt used for image generation.",
        required=True,
    )
    parser.add_argument(
        "--sampler",
        type=str,
        help="Name of the desired sampler for image generation.",
        required=False,
    )
    parser.add_argument(
        "--scheduler",
        type=str,
        help="Type of scheduler for image generation.",
        required=False,
    )
    parser.add_argument(
        "--dimensions",
        type=str,
        help="Desired final image dimensions in format: x,y",
        required=False,
    )
    parser.add_argument(
        "--denoise",
        type=float,
        help="Balance between noise reduction and detail preservation.",
        required=False,
    )
    parser.add_argument(
        "--steps", type=int, help="Sampling steps for image generation.", required=False
    )
    parser.add_argument(
        "--cfg", type=float, help="Creativity level of AI's generation.", required=False
    )
    parser.add_argument(
        "--count", type=int, help="Number of images to generate.", required=False
    )

    return parser.parse_args(args_list)


def worker(task_queue):
    while True:
        task = task_queue.get()
        if task is None:
            task_queue.task_done()
            break

        try:
            generate(task)
            logging.info("Task completed successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        task_queue.task_done()


def input_handler(input_queue, task_queue):
    while True:
        cmd = input_queue.get()
        if cmd == "exit":
            task_queue.put(None)
            input_queue.task_done()
            break

        try:
            args_list = cmd.split()
            args = parse_args(args_list)

            if args.dimensions:
                x, y = map(int, args.dimensions.split(","))
            else:
                x, y = 1024, 1024

            task = GenerationParameters(
                image=args.image,
                positive_prompt=args.prompt,
                sampler=args.sampler if args.sampler else "dpmpp_3m_sde_gpu",
                scheduler=args.scheduler if args.scheduler else "exponential",
                dimensions=Dimensions(x, y),
                denoise=args.denoise if args.denoise is not None else 1.0,
                steps=args.steps if args.steps is not None else 35,
                cfg=args.cfg if args.cfg is not None else 7.0,
                iterations=args.count if args.count is not None else 5,
            )

            task_queue.put(task)

        except Exception as e:
            logging.error(f"An error occurred: {e}")

        input_queue.task_done()


def main():
    input_queue: Queue = Queue()
    task_queue: Queue[GenerationParameters] = Queue()

    input_thread = threading.Thread(
        target=input_handler, args=(input_queue, task_queue), daemon=True
    )
    input_thread.start()

    worker_thread = threading.Thread(
        target=worker, args=(task_queue,), daemon=True)
    worker_thread.start()

    print("--== A-Eye Image Generation CLI ==--")
    while True:
        user_input = input(
            "Enter command (or 'exit' to stop): ").strip().lower()

        if user_input == "exit":
            break

        input_queue.put(user_input)

    input_thread.join()
    task_queue.put(None)
    worker_thread.join()


if __name__ == "__main__":
    main()
