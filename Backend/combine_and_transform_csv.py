import pandas as pd


def combine_and_transform_csv(df1_path, df2_path, output_path):
    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)

    df_combined = pd.concat([df1, df2], axis=1)
    df_combined = df_combined.reindex(df2.index)
    df_combined.drop(columns=['true_label'], inplace=True)
    df_combined.index += 1

    def get_class_names():
        # สร้างรายชื่อคลาสตามลำดับที่คุณต้องการ
        return ["Buy_Aciton", "Class 0 Aciton", "Dead_Aciton", "Defuse Aciton", "Orb Aciton", "Plant Aciton", "Shoot_Aciton", "Skill_Aciton"]

    # ใช้ฟังก์ชันเพื่อรับชื่อคลาส
    class_names = get_class_names()

    # Assuming 'predicted_label' is the name of the column containing predicted labels
    # Assuming 'class_names' is a list containing the class names
    class_names_dict = {i: class_name for i,
                        class_name in enumerate(class_names)}

    # Add a new column 'predicted_class_names' to df_combined
    df_combined['predicted_class_names'] = df_combined['predicted_label'].map(
        class_names_dict)

    # เรียกใช้ชื่อคลาสตามตำแหน่งที่ทำนายได้
    for label in df_combined['predicted_label']:
        print(class_names[label])
    df_combined = df_combined.reindex(
        columns=['clip_start_times', 'predicted_class_names'])

    # พิมพ์ DataFrame ที่เกิดขึ้น
    df_combined

    df_combined.to_csv(output_path, index=False)
