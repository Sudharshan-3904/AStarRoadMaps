import core.roadmap_generator as rmg


class CLI:
    def run(self):
        while True:
            print("Welcom eto roadmap creator !!!. This is an interactive tool to create roadmaps.")
            
            if input("To quit, enter quit: "):
                break
            
            map_topic = input("Enter the topic: ")
            map_level = input("Enter the Level ( Begginer, Intermediate, Advanced, Refresher, Full): ").lower()

            latest_one = rmg.create_new_roadmap(topic=map_topic, level=map_level)
            print(latest_one)

if __name__ == '__main__':
    runner_obj = CLI()
    runner_obj.run()
