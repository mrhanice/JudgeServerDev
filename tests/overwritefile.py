
if __name__ == '__main__':
    src = '''package com.hadoop;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

class WcMapper extends Mapper<LongWritable, Text,Text, IntWritable> {
    private Text word = new Text();
    private IntWritable one = new IntWritable(1);

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        //拿到这一行数据
        String line = value.toString();
        String[] words = line.split(" ");
        for(String word: words) {
            this.word.set(word);
            context.write(this.word,one);
        }
    }
}

class WcReducer extends Reducer<Text, IntWritable,Text, IntWritable> {
    private IntWritable totol = new IntWritable();

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        int sum = 0;
        for(IntWritable value: values) {
            sum += value.get();
        }
        totol.set(sum);
        context.write(key,totol);
    }
}

public class Main {

    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {

        Configuration conf =new Configuration();
        //String[] otherArgs =new GenericOptionsParser(conf, args).getRemainingArgs();

        //(1) 获取一个job实例
        Job job = Job.getInstance(conf);
        //(2) 设置我们的类路径(ClassPath)
        job.setJarByClass(Main.class);
        //(3) 设置Mapper和Reducer
        job.setMapperClass(WcMapper.class);
        job.setReducerClass(WcReducer.class);
        //(4) 设置Mapper和Reducer输出类型
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        //(5)设置输入输出数据
        FileInputFormat.setInputPaths(job,new Path(args[0]));
        FileOutputFormat.setOutputPath(job,new Path(args[1]));

        //(6) 提交我们的job
        boolean b = job.waitForCompletion(true);
        System.exit(b ? 0 : 1);
    }
}'''
    with open('in', "w", encoding="utf-8") as f:  # 创建Main.java文件，并把源代码src写入该文件
        f.write(src)